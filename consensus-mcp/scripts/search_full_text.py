#!/usr/bin/env python3
"""Search Consensus for query-relevant full-text excerpts using the REST API."""

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


ENDPOINT = "https://api.consensus.app/v1/search"
DEFAULT_KEY_FILE = Path("~/.config/consensus/api-key")


class SearchError(Exception):
    """An error whose message is safe to display without exposing credentials."""


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def load_api_key(key_file):
    key = os.environ.get("CONSENSUS_API_KEY", "").strip()
    if not key:
        try:
            key = Path(key_file).expanduser().read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            raise SearchError(
                "Set CONSENSUS_API_KEY or provide a readable UTF-8 --key-file."
            ) from None
    if not key or "\n" in key or "\r" in key:
        raise SearchError("API key is empty or has an invalid format.")
    return key


def search(query, page_size, open_access, key):
    params = {
        "query": query,
        "include_full_text_chunks": "true",
        "page_size": page_size,
    }
    if open_access:
        params["open_access"] = "true"
    request = Request(
        ENDPOINT + "?" + urlencode(params),
        headers={"x-api-key": key, "Accept": "application/json"},
        method="GET",
    )
    try:
        with build_opener(NoRedirects()).open(request, timeout=30) as response:
            data = json.loads(response.read())
    except HTTPError as error:
        status = error.code
        error.close()
        if 300 <= status < 400:
            message = "Redirect refused; API credentials were not forwarded."
        else:
            message = {
                401: "Authentication failed; check the API key and account.",
                402: "Account billing requires attention.",
                403: "Access denied; check the key's account and paid-plan entitlement.",
                429: "Rate or usage limit reached; no automatic retry was attempted.",
            }.get(status, "Consensus request failed.")
        raise SearchError(f"HTTP {status}: {message}") from None
    except (json.JSONDecodeError, UnicodeError):
        raise SearchError("Consensus returned invalid JSON or text encoding.") from None
    except (URLError, OSError, ValueError):
        raise SearchError("Consensus request failed; check connectivity and key format.") from None

    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise SearchError("Consensus response must contain a results array.")
    for paper in data["results"]:
        if not isinstance(paper, dict):
            raise SearchError("Consensus results must contain paper objects.")
        chunks = paper.get("full_text_chunks")
        if chunks is not None and (
            not isinstance(chunks, list)
            or any(not isinstance(chunk, str) for chunk in chunks)
        ):
            raise SearchError("Consensus full_text_chunks must be null or an array of strings.")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Specific research question or passage to find")
    parser.add_argument("--page-size", type=positive_int, default=3)
    parser.add_argument("--open-access", action="store_true", help="Limit to open-access papers")
    parser.add_argument(
        "--key-file", type=Path, default=DEFAULT_KEY_FILE,
        help="API key file (default: ~/.config/consensus/api-key); CONSENSUS_API_KEY takes precedence",
    )
    args = parser.parse_args(argv)
    try:
        data = search(args.query, args.page_size, args.open_access, load_api_key(args.key_file))
    except SearchError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
