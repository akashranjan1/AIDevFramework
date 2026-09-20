#!/usr/bin/env python3
"""Retrieve one Jira Cloud issue using credentials supplied through environment variables."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


FIELDS = "summary,description,issuetype,status,priority,labels,components,fixVersions,issuelinks,subtasks,attachment,comment"


def required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} is required. Set it in your terminal or secret manager; do not commit it.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a Jira Cloud story as JSON.")
    parser.add_argument("issue_key", help="Jira key, for example ABCD-123")
    parser.add_argument("--output", type=Path, help="File to receive the JSON response")
    args = parser.parse_args()

    try:
        base_url = required("JIRA_BASE_URL").rstrip("/")
        email = required("JIRA_EMAIL")
        token = required("JIRA_API_TOKEN")
        if not base_url.startswith("https://"):
            raise ValueError("JIRA_BASE_URL must begin with https://")
        credentials = base64.b64encode(f"{email}:{token}".encode()).decode()
        url = f"{base_url}/rest/api/3/issue/{quote(args.issue_key)}?fields={FIELDS}"
        request = Request(url, headers={"Accept": "application/json", "Authorization": f"Basic {credentials}"})
        with urlopen(request, timeout=30) as response:
            story = json.load(response)
    except (ValueError, HTTPError, URLError) as error:
        detail = error.read().decode(errors="replace") if isinstance(error, HTTPError) else str(error)
        print(f"Jira retrieval failed: {detail}", file=sys.stderr)
        return 1

    output = args.output
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(story, indent=2), encoding="utf-8")
        print(f"Saved Jira story snapshot: {output}")
    else:
        print(json.dumps(story, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
