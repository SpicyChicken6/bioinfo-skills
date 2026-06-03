#!/usr/bin/env python3
"""Run MSigDB over-representation analysis with GSEApy."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

POS_COLOR = "#ff5a70"
NEG_COLOR = "#9ed8ec"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run offline ORA with GSEApy gene sets retrieved from MSigDB."
    )
    parser.add_argument("--genes", help="Single foreground gene list: txt, csv, or tsv.")
    parser.add_argument(
        "--up-genes",
        help="Foreground genes up in the positive/right-side group for paired ORA plots.",
    )
    parser.add_argument(
        "--down-genes",
        help="Foreground genes up in the negative/left-side group for paired ORA plots.",
    )
    parser.add_argument("--gene-column", help="Column name or zero-based index for table input.")
    parser.add_argument(
        "--up-gene-column",
        help="Column name or zero-based index for --up-genes; defaults to --gene-column.",
    )
    parser.add_argument(
        "--down-gene-column",
        help="Column name or zero-based index for --down-genes; defaults to --gene-column.",
    )
    parser.add_argument("--no-header", action="store_true", help="Read csv/tsv files without a header row.")
    parser.add_argument(
        "--background",
        help=(
            "Background as a gene-list file, integer universe size, or BioMart dataset "
            "name. If omitted, GSEApy uses genes from the selected gene sets."
        ),
    )
    parser.add_argument(
        "--background-column",
        help="Column name or zero-based index for background table input.",
    )
    parser.add_argument(
        "--species",
        default="human",
        help="Species: human/hs or mouse/mm. Default: human.",
    )
    parser.add_argument(
        "--dbver",
        default="latest",
        help="MSigDB version such as 2024.1.Hs or 2023.1.Mm. Use latest/auto to infer.",
    )
    parser.add_argument(
        "--category",
        action="append",
        help="MSigDB category. Repeat or comma-separate. Defaults to h.all for human, mh.all for mouse.",
    )
    parser.add_argument(
        "--case",
        choices=["auto", "preserve", "upper", "lower", "title"],
        default="auto",
        help="Gene case normalization. auto uppercases human and preserves mouse.",
    )
    parser.add_argument("--cutoff", type=float, default=0.05, help="Adjusted p-value cutoff.")
    parser.add_argument("--top", type=int, default=20, help="Number of top terms for summary and plot.")
    parser.add_argument(
        "--plot-column",
        default="P-value",
        choices=["P-value", "Adjusted P-value"],
        help="P-value column used for top-term plots. Default: P-value.",
    )
    parser.add_argument(
        "--plot-dpi",
        type=int,
        default=300,
        help="DPI for raster PNG plot outputs. Default: 300.",
    )
    parser.add_argument(
        "--plot-threshold",
        type=float,
        default=0.05,
        help="P-value threshold to mark on plot x-axes. Default: 0.05.",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip the vector PDF companion plot generated for each PNG.",
    )
    parser.add_argument(
        "--positive-label",
        default="Contrast",
        help="Right-side label for paired plots; --up-genes are positive.",
    )
    parser.add_argument(
        "--negative-label",
        default="Control",
        help="Left-side label for paired plots; --down-genes are negative.",
    )
    parser.add_argument(
        "--contrast-label",
        default="contrast",
        help="Short label used in paired plot filenames and summaries.",
    )
    parser.add_argument("--outdir", default="ora_results", help="Output directory.")
    parser.add_argument("--no-plot", action="store_true", help="Skip top-term PNG plot.")
    parser.add_argument("--verbose", action="store_true", help="Pass verbose=True to GSEApy.")
    parser.add_argument("--list-dbver", action="store_true", help="List MSigDB versions and exit unless --genes is also set.")
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List categories for --dbver/--species and exit unless --genes is also set.",
    )
    return parser.parse_args()


def import_dependencies(need_plot: bool):
    missing: list[str] = []
    try:
        import pandas as pd  # type: ignore
    except ModuleNotFoundError:
        pd = None
        missing.append("pandas")
    try:
        import gseapy as gp  # type: ignore
        from gseapy import Msigdb  # type: ignore
    except ModuleNotFoundError:
        gp = None
        Msigdb = None
        missing.append("gseapy")
    plt = None
    if need_plot:
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt_import  # type: ignore

            plt = plt_import
        except ModuleNotFoundError:
            missing.append("matplotlib")
    if missing:
        packages = " ".join(sorted(set(missing)))
        raise SystemExit(
            "Missing required Python packages: "
            f"{packages}\nInstall with: python -m pip install gseapy pandas matplotlib"
        )
    return pd, gp, Msigdb, plt


def normalize_species(species: str) -> dict[str, str]:
    value = species.strip().lower().replace("_", " ")
    human = {"human", "hs", "hsa", "homo sapiens", "h. sapiens"}
    mouse = {"mouse", "mm", "mmu", "mus musculus", "m. musculus"}
    if value in human:
        return {
            "name": "human",
            "suffix": "Hs",
            "default_category": "h.all",
            "auto_case": "upper",
        }
    if value in mouse:
        return {
            "name": "mouse",
            "suffix": "Mm",
            "default_category": "mh.all",
            "auto_case": "preserve",
        }
    raise ValueError("Unsupported species. Use human/hs or mouse/mm.")


def expand_values(values: Iterable[str] | None) -> list[str]:
    expanded: list[str] = []
    for value in values or []:
        expanded.extend(part.strip() for part in value.split(",") if part.strip())
    return expanded


def version_key(dbver: str) -> tuple[list[int], str]:
    return ([int(part) for part in re.findall(r"\d+", str(dbver))], str(dbver))


def as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, dict):
        return [str(key) for key in value.keys()]
    return [str(item) for item in value]


def resolve_dbver(msig: Any, requested: str, suffix: str) -> str:
    if requested.lower() not in {"latest", "auto"}:
        return requested
    versions = as_string_list(msig.list_dbver())
    matches = [version for version in versions if version.endswith(f".{suffix}")]
    if not matches:
        raise ValueError(f"No MSigDB versions ending in .{suffix} were returned by GSEApy.")
    return sorted(matches, key=version_key)[-1]


def read_plain_gene_file(path: Path) -> list[str]:
    genes: list[str] = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        genes.append(re.split(r"[\t, ]+", line)[0].strip())
    return genes


def select_column(df: Any, column: str | None) -> Any:
    if column is None:
        return df.iloc[:, 0]
    if column.isdigit():
        return df.iloc[:, int(column)]
    if column in df.columns:
        return df[column]
    raise ValueError(f"Column {column!r} not found. Available columns: {list(df.columns)}")


def read_gene_file(path_text: str, column: str | None, no_header: bool, pd: Any) -> list[str]:
    path = Path(path_text).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Gene list file does not exist: {path}")
    suffix = path.suffix.lower()
    if column is None and suffix not in {".csv", ".tsv", ".tab"}:
        return read_plain_gene_file(path)
    sep = "," if suffix == ".csv" else "\t"
    header = None if no_header else "infer"
    df = pd.read_csv(path, sep=sep, comment="#", header=header)
    return [str(value).strip() for value in select_column(df, column).tolist()]


def normalize_genes(genes: Iterable[Any], case_mode: str, species_info: dict[str, str]) -> list[str]:
    selected_case = species_info["auto_case"] if case_mode == "auto" else case_mode
    seen: set[str] = set()
    cleaned: list[str] = []
    for value in genes:
        if value is None:
            continue
        gene = str(value).strip()
        if not gene or gene.lower() == "nan":
            continue
        if selected_case == "upper":
            gene = gene.upper()
        elif selected_case == "lower":
            gene = gene.lower()
        elif selected_case == "title":
            gene = gene.title()
        if gene not in seen:
            seen.add(gene)
            cleaned.append(gene)
    return cleaned


def parse_background(args: argparse.Namespace, pd: Any, species_info: dict[str, str]) -> tuple[Any, dict[str, Any]]:
    if not args.background:
        return None, {"kind": "gene_sets_union", "detail": "GSEApy default"}

    value = args.background.strip()
    path = Path(value).expanduser()
    if path.exists():
        genes = read_gene_file(value, args.background_column, args.no_header, pd)
        genes = normalize_genes(genes, args.case, species_info)
        return genes, {"kind": "gene_list", "path": str(path), "unique_genes": len(genes)}

    if re.fullmatch(r"\d+", value):
        return int(value), {"kind": "integer_universe", "size": int(value)}

    return value, {"kind": "biomart_dataset", "dataset": value}


def add_overlap_columns(df: Any, pd: Any) -> Any:
    if "Overlap" not in df.columns:
        return df
    extracted = df["Overlap"].astype(str).str.extract(r"(\d+)\s*/\s*(\d+)")
    df["Overlap_count"] = pd.to_numeric(extracted[0], errors="coerce")
    df["Gene_set_size"] = pd.to_numeric(extracted[1], errors="coerce")
    return df


def sort_results(df: Any) -> Any:
    sort_cols = [col for col in ["Adjusted P-value", "P-value"] if col in df.columns]
    if not sort_cols:
        return df
    return df.sort_values(sort_cols, ascending=True, kind="mergesort")


def sort_by_column(df: Any, column: str) -> Any:
    if column not in df.columns:
        return df
    return df.sort_values(column, ascending=True, kind="mergesort")


def finite_neg_log10(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numeric):
        return 0.0
    return -math.log10(max(numeric, 1e-300))


def threshold_neg_log10(threshold: float | None) -> float | None:
    if threshold is None:
        return None
    try:
        numeric = float(threshold)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric) or numeric <= 0 or numeric >= 1:
        return None
    return -math.log10(numeric)


def logp_axis_label(column: str, threshold: float | None) -> str:
    base = "-log10(p)" if column == "P-value" else "-log10(adj. p)"
    if threshold_neg_log10(threshold) is None:
        return base
    threshold_text = f"{float(threshold):g}"
    suffix = f"p>{threshold_text}" if column == "P-value" else f"threshold={threshold_text}"
    return f"{base} ({suffix})"


def trim_label(label: Any, max_chars: int = 80) -> str:
    text = str(label)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "..."


def clean_axes(ax: Any) -> None:
    ax.grid(False)
    ax.xaxis.grid(False, which="both")
    ax.yaxis.grid(False, which="both")
    for gridline in ax.get_xgridlines() + ax.get_ygridlines():
        gridline.set_visible(False)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_linewidth(1.6)


def safe_filename(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", text.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_.")
    return cleaned or "category"


def save_figure(fig: Any, output_path: Path, dpi: int, write_pdf: bool, bbox_inches: str | None = None) -> str | None:
    fig.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
    if not write_pdf:
        return None
    pdf_path = output_path.with_suffix(".pdf")
    fig.savefig(pdf_path, bbox_inches=bbox_inches)
    return str(pdf_path)


def add_threshold_markers(
    ax: Any,
    threshold: float,
    signed: bool,
) -> None:
    threshold_value = threshold_neg_log10(threshold)
    if threshold_value is None:
        return
    values = [-threshold_value, threshold_value] if signed else [threshold_value]
    for value in values:
        ax.axvline(
            value,
            color="black",
            lw=1.0,
            linestyle=(0, (4, 3)),
            alpha=0.65,
            zorder=8,
        )


def write_plot(
    df: Any,
    output_path: Path,
    top_n: int,
    cutoff: float,
    plot_threshold: float,
    dpi: int,
    write_pdf: bool,
    plt: Any,
) -> str | None:
    if df.empty or "Adjusted P-value" not in df.columns:
        return None
    plot_df = df.copy()
    significant = plot_df[plot_df["Adjusted P-value"] <= cutoff]
    if not significant.empty:
        plot_df = significant
    plot_df = sort_results(plot_df).head(top_n).copy()
    if plot_df.empty:
        return None

    plot_df["neg_log10_adjusted_p"] = plot_df["Adjusted P-value"].map(finite_neg_log10)
    plot_df = plot_df.iloc[::-1]
    labels = [trim_label(term) for term in plot_df["Term"]]
    categories = plot_df["MSigDB_category"].astype(str).tolist()
    unique_categories = list(dict.fromkeys(categories))
    palette = plt.get_cmap("tab10")
    colors = {cat: palette(i % 10) for i, cat in enumerate(unique_categories)}
    bar_colors = [colors[cat] for cat in categories]

    height = max(4.0, 0.34 * len(plot_df) + 1.4)
    fig, ax = plt.subplots(figsize=(10, height))
    ax.barh(labels, plot_df["neg_log10_adjusted_p"], color=bar_colors)
    ax.set_xlabel(logp_axis_label("Adjusted P-value", plot_threshold), labelpad=8)
    ax.set_ylabel("")
    ax.set_title("Top ORA terms")
    clean_axes(ax)
    threshold_value = threshold_neg_log10(plot_threshold)
    if threshold_value is not None:
        ax.set_xlim(right=max(ax.get_xlim()[1], threshold_value * 1.15))
        add_threshold_markers(ax, plot_threshold, signed=False)
    if len(unique_categories) > 1:
        handles = [
            plt.Line2D([0], [0], color=colors[cat], lw=6, label=cat)
            for cat in unique_categories
        ]
        ax.legend(handles=handles, title="MSigDB category", loc="lower right")
    fig.tight_layout()
    pdf_path = save_figure(fig, output_path, dpi=dpi, write_pdf=write_pdf)
    plt.close(fig)
    return pdf_path


def signed_top_terms(df: Any, sign: int, top_n: int, column: str, pd: Any) -> Any:
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=["Term", "signed_logp"])
    top = sort_by_column(df, column).head(top_n).copy()
    top["signed_logp"] = [
        sign * finite_neg_log10(value) for value in top[column].tolist()
    ]
    keep = ["Term", "signed_logp"]
    if "Genes" in top.columns:
        keep.append("Genes")
    return top.loc[:, keep]


def write_combined_direction_plot(
    up_df: Any,
    down_df: Any,
    output_path: Path,
    top_n: int,
    column: str,
    positive_label: str,
    negative_label: str,
    plot_threshold: float,
    dpi: int,
    write_pdf: bool,
    pd: Any,
    plt: Any,
) -> str | None:
    from matplotlib.patches import FancyArrowPatch

    up_terms = signed_top_terms(up_df, +1, top_n, column, pd)
    down_terms = signed_top_terms(down_df, -1, top_n, column, pd)
    down_terms = down_terms.iloc[::-1].reset_index(drop=True)
    combined = pd.concat([up_terms, down_terms], ignore_index=True)
    if combined.empty:
        return None
    vals = combined["signed_logp"].tolist()
    terms = [trim_label(term, max_chars=54) for term in combined["Term"].tolist()]
    xmax = max(max(abs(float(value)) for value in vals) * 1.15, 1.0)
    threshold_value = threshold_neg_log10(plot_threshold)
    if threshold_value is not None:
        xmax = max(xmax, threshold_value * 1.15)

    fig, ax = plt.subplots(figsize=(6.4, max(4.2, 0.32 * len(terms))))
    y = list(range(len(terms)))
    colors = [POS_COLOR if value >= 0 else NEG_COLOR for value in vals]
    ax.barh(y, vals, color=colors, edgecolor="black", linewidth=0.6, zorder=2)
    ax.axvline(0, lw=1.6, color="black", zorder=20)
    ax.set_yticks(y)
    ax.set_yticklabels(terms)
    ax.invert_yaxis()
    ax.set_xlim(-xmax, xmax)
    ax.set_xlabel(logp_axis_label(column, plot_threshold), labelpad=8)
    clean_axes(ax)
    add_threshold_markers(ax, plot_threshold, signed=True)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_linewidth(1.6)
    ax.tick_params(axis="y", length=8, width=1.6, direction="out", color="black", pad=10)

    arrow_y, label_y = 1.03, 1.10
    gap_side, gap_center = 0.05, 0.10
    tip_extension = 0.025
    left_a, left_b = (0 + gap_side, 0.5 - gap_center / 2)
    right_a, right_b = (1 - gap_side, 0.5 + gap_center / 2)
    for a, b in ((left_b, left_a), (right_b, right_a)):
        direction = 1 if b > a else -1
        ax.add_patch(
            FancyArrowPatch(
                posA=(a, arrow_y),
                posB=(b + direction * tip_extension, arrow_y),
                arrowstyle="-|>,head_length=0.9,head_width=0.45",
                lw=0.8,
                mutation_scale=18,
                color="black",
                transform=ax.transAxes,
                clip_on=False,
                shrinkA=0,
                shrinkB=0,
                joinstyle="miter",
            )
        )
    ax.text(
        (left_a + left_b) / 2,
        label_y,
        negative_label,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=10,
    )
    ax.text(
        (right_a + right_b) / 2,
        label_y,
        positive_label,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=10,
    )
    fig.tight_layout()
    pdf_path = save_figure(fig, output_path, dpi=dpi, write_pdf=write_pdf, bbox_inches="tight")
    plt.close(fig)
    return pdf_path


def write_single_direction_plot(
    df: Any,
    output_path: Path,
    title: str,
    top_n: int,
    column: str,
    color: str,
    plot_threshold: float,
    dpi: int,
    write_pdf: bool,
    plt: Any,
) -> str | None:
    if df.empty or column not in df.columns:
        return None
    top = sort_by_column(df, column).head(top_n).copy()
    if top.empty:
        return None
    top["logp"] = [finite_neg_log10(value) for value in top[column].tolist()]
    top = top.sort_values("logp", ascending=True, kind="mergesort")

    fig, ax = plt.subplots(figsize=(6.4, max(3, 0.32 * len(top))))
    labels = [trim_label(term, max_chars=54) for term in top["Term"].tolist()]
    ax.barh(labels, top["logp"], color=color, edgecolor="black", linewidth=0.6)
    ax.set_xlabel(logp_axis_label(column, plot_threshold), labelpad=8)
    ax.set_title(title, fontsize=10)
    clean_axes(ax)
    threshold_value = threshold_neg_log10(plot_threshold)
    if threshold_value is not None:
        ax.set_xlim(right=max(ax.get_xlim()[1], threshold_value * 1.15))
        add_threshold_markers(ax, plot_threshold, signed=False)
    fig.tight_layout()
    pdf_path = save_figure(fig, output_path, dpi=dpi, write_pdf=write_pdf, bbox_inches="tight")
    plt.close(fig)
    return pdf_path


def write_direction_plots(
    combined: Any,
    outdir: Path,
    categories: list[str],
    args: argparse.Namespace,
    pd: Any,
    plt: Any,
) -> tuple[list[str], list[str]]:
    if combined.empty or "Direction" not in combined.columns:
        return [], []
    plot_paths: list[str] = []
    pdf_paths: list[str] = []
    for category in categories:
        category_df = combined[combined["MSigDB_category"] == category]
        up_df = category_df[category_df["Direction"] == "up"]
        down_df = category_df[category_df["Direction"] == "down"]
        category_name = safe_filename(category)
        contrast_name = safe_filename(args.contrast_label)
        if not up_df.empty and not down_df.empty:
            path = outdir / f"ora_{contrast_name}_combined_{category_name}_top.png"
            pdf_path = write_combined_direction_plot(
                up_df=up_df,
                down_df=down_df,
                output_path=path,
                top_n=args.top,
                column=args.plot_column,
                positive_label=args.positive_label,
                negative_label=args.negative_label,
                plot_threshold=args.plot_threshold,
                dpi=args.plot_dpi,
                write_pdf=not args.no_pdf,
                pd=pd,
                plt=plt,
            )
            if path.exists():
                plot_paths.append(str(path))
            if pdf_path:
                pdf_paths.append(pdf_path)
        elif not up_df.empty:
            path = outdir / f"ora_{contrast_name}_up_{category_name}_top.png"
            pdf_path = write_single_direction_plot(
                df=up_df,
                output_path=path,
                title=f"up in {args.positive_label} - {category}",
                top_n=args.top,
                column=args.plot_column,
                color=POS_COLOR,
                plot_threshold=args.plot_threshold,
                dpi=args.plot_dpi,
                write_pdf=not args.no_pdf,
                plt=plt,
            )
            if path.exists():
                plot_paths.append(str(path))
            if pdf_path:
                pdf_paths.append(pdf_path)
        elif not down_df.empty:
            path = outdir / f"ora_{contrast_name}_down_{category_name}_top.png"
            pdf_path = write_single_direction_plot(
                df=down_df,
                output_path=path,
                title=f"up in {args.negative_label} - {category}",
                top_n=args.top,
                column=args.plot_column,
                color=NEG_COLOR,
                plot_threshold=args.plot_threshold,
                dpi=args.plot_dpi,
                write_pdf=not args.no_pdf,
                plt=plt,
            )
            if path.exists():
                plot_paths.append(str(path))
            if pdf_path:
                pdf_paths.append(pdf_path)
    return plot_paths, pdf_paths


def compact_top_terms(df: Any, top_n: int) -> list[dict[str, Any]]:
    columns = [
        "MSigDB_category",
        "Term",
        "Adjusted P-value",
        "P-value",
        "Odds Ratio",
        "Overlap",
        "Genes",
    ]
    present = [col for col in columns if col in df.columns]
    if not present:
        return []
    top = sort_results(df).head(top_n).loc[:, present].copy()
    top = top.where(top.notna(), None)
    return top.to_dict(orient="records")


def enrich_foreground(
    gp: Any,
    foreground: list[str],
    gmt: dict[str, list[str]],
    background: Any,
    args: argparse.Namespace,
) -> Any:
    enr = gp.enrich(
        gene_list=foreground,
        gene_sets=gmt,
        background=background,
        outdir=None,
        cutoff=args.cutoff,
        no_plot=True,
        verbose=args.verbose,
    )
    result_df = getattr(enr, "results", None)
    if result_df is None:
        result_df = getattr(enr, "res2d")
    return result_df.copy()


def read_foreground(
    path_text: str,
    column: str | None,
    args: argparse.Namespace,
    pd: Any,
    species_info: dict[str, str],
) -> tuple[list[str], list[str], dict[str, Any]]:
    raw = read_gene_file(path_text, column, args.no_header, pd)
    genes = normalize_genes(raw, args.case, species_info)
    if len(genes) < 2:
        raise ValueError(f"Need at least two foreground genes after cleaning: {path_text}")
    summary = {
        "path": str(Path(path_text).expanduser()),
        "input_rows": len(raw),
        "unique_genes": len(genes),
    }
    return raw, genes, summary


def main() -> int:
    args = parse_args()
    paired_mode = bool(args.up_genes or args.down_genes)
    metadata_only = (args.list_dbver or args.list_categories) and not args.genes and not paired_mode
    pd, gp, Msigdb, plt = import_dependencies(need_plot=not args.no_plot and not metadata_only)
    species_info = normalize_species(args.species)
    msig = Msigdb()

    if args.list_dbver:
        for dbver in as_string_list(msig.list_dbver()):
            print(dbver)
        if not args.genes and not paired_mode and not args.list_categories:
            return 0

    dbver = resolve_dbver(msig, args.dbver, species_info["suffix"])

    if args.list_categories:
        for category in as_string_list(msig.list_category(dbver=dbver)):
            print(category)
        if not args.genes and not paired_mode:
            return 0

    if args.genes and paired_mode:
        raise SystemExit("Use either --genes or --up-genes/--down-genes, not both.")
    if not args.genes and not paired_mode:
        raise SystemExit("--genes or --up-genes/--down-genes is required unless only listing MSigDB metadata.")

    outdir = Path(args.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    categories = expand_values(args.category) or [species_info["default_category"]]
    background, background_summary = parse_background(args, pd, species_info)

    foregrounds: list[dict[str, Any]] = []
    foreground_summary: dict[str, Any] = {}
    if paired_mode:
        if args.up_genes:
            _, genes, summary = read_foreground(
                args.up_genes,
                args.up_gene_column or args.gene_column,
                args,
                pd,
                species_info,
            )
            foregrounds.append(
                {
                    "direction": "up",
                    "direction_label": args.positive_label,
                    "genes": genes,
                }
            )
            foreground_summary["up"] = summary
        if args.down_genes:
            _, genes, summary = read_foreground(
                args.down_genes,
                args.down_gene_column or args.gene_column,
                args,
                pd,
                species_info,
            )
            foregrounds.append(
                {
                    "direction": "down",
                    "direction_label": args.negative_label,
                    "genes": genes,
                }
            )
            foreground_summary["down"] = summary
    else:
        _, genes, summary = read_foreground(
            args.genes,
            args.gene_column,
            args,
            pd,
            species_info,
        )
        foregrounds.append({"direction": None, "direction_label": None, "genes": genes})
        foreground_summary = summary

    frames: list[Any] = []
    category_gene_set_counts: dict[str, int] = {}
    for category in categories:
        gmt = msig.get_gmt(category=category, dbver=dbver)
        if not gmt:
            raise ValueError(f"No gene sets returned for category={category!r}, dbver={dbver!r}.")
        category_gene_set_counts[category] = len(gmt)
        for foreground_info in foregrounds:
            result_df = enrich_foreground(
                gp=gp,
                foreground=foreground_info["genes"],
                gmt=gmt,
                background=background,
                args=args,
            )
            result_df.insert(0, "MSigDB_category", category)
            result_df.insert(0, "MSigDB_dbver", dbver)
            if paired_mode:
                result_df.insert(2, "Direction", foreground_info["direction"])
                result_df.insert(3, "Direction_label", foreground_info["direction_label"])
            result_df = add_overlap_columns(result_df, pd)
            frames.append(result_df)

    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    combined = sort_results(combined)
    results_tsv = outdir / "ora_results.tsv"
    results_csv = outdir / "ora_results.csv"
    significant_tsv = outdir / "ora_significant.tsv"
    combined.to_csv(results_tsv, sep="\t", index=False)
    combined.to_csv(results_csv, index=False)

    if "Adjusted P-value" in combined.columns:
        significant = combined[combined["Adjusted P-value"] <= args.cutoff]
    else:
        significant = combined.iloc[0:0]
    significant.to_csv(significant_tsv, sep="\t", index=False)

    plot_path = outdir / "top_terms.png"
    direction_plot_paths: list[str] = []
    direction_plot_pdf_paths: list[str] = []
    top_terms_pdf_path: str | None = None
    if not args.no_plot and plt is not None:
        if paired_mode:
            direction_plot_paths, direction_plot_pdf_paths = write_direction_plots(
                combined=combined,
                outdir=outdir,
                categories=categories,
                args=args,
                pd=pd,
                plt=plt,
            )
        else:
            top_terms_pdf_path = write_plot(
                combined,
                plot_path,
                args.top,
                args.cutoff,
                args.plot_threshold,
                args.plot_dpi,
                not args.no_pdf,
                plt,
            )

    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "gseapy_version": getattr(gp, "__version__", None),
        "species": species_info["name"],
        "msigdb_dbver": dbver,
        "msigdb_categories": categories,
        "msigdb_gene_set_counts": category_gene_set_counts,
        "case_mode": args.case,
        "foreground": foreground_summary,
        "background": background_summary,
        "cutoff": args.cutoff,
        "plot_column": args.plot_column,
        "plot_threshold": args.plot_threshold,
        "plot_dpi": args.plot_dpi,
        "pdf_plots": not args.no_pdf,
        "result_rows": int(len(combined)),
        "significant_rows": int(len(significant)),
        "outputs": {
            "results_tsv": str(results_tsv),
            "results_csv": str(results_csv),
            "significant_tsv": str(significant_tsv),
            "top_terms_png": str(plot_path) if plot_path.exists() else None,
            "top_terms_pdf": top_terms_pdf_path,
            "direction_plots": direction_plot_paths,
            "direction_plot_pdfs": direction_plot_pdf_paths,
        },
        "top_terms": compact_top_terms(combined, args.top),
    }
    summary_path = outdir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str) + "\n")

    print(f"Wrote {results_tsv}")
    print(f"Wrote {significant_tsv}")
    print(f"Wrote {summary_path}")
    if plot_path.exists():
        print(f"Wrote {plot_path}")
    if top_terms_pdf_path:
        print(f"Wrote {top_terms_pdf_path}")
    for path in direction_plot_paths:
        print(f"Wrote {path}")
    for path in direction_plot_pdf_paths:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit("Interrupted")
    except Exception as exc:
        raise SystemExit(f"ERROR: {exc}")
