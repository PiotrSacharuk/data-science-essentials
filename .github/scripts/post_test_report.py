#!/usr/bin/env python3
"""Read pytest JSON report and post a short summary as a PR comment.

This script expects the following environment variables:
- GITHUB_TOKEN
- REPO (owner/repo)
- PR_NUMBER
- GITHUB_API_URL (optional, defaults to https://api.github.com)
"""
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests not installed; please install requests in the workflow step")
    sys.exit(2)


def load_report(path="report.json"):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def build_body(data):
    summary = data.get("summary", {})
    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("error", 0)
    skipped = summary.get("skipped", 0)

    lines = [
        "## Test summary",
        "",
        f"- Total tests: **{total}**",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        f"- Errors: **{errors}**",
        f"- Skipped: **{skipped}**",
        "",
    ]

    failures = []
    for tc in data.get("tests", []):
        if tc.get("outcome") in ("failed", "error"):
            nodeid = tc.get("nodeid") or tc.get("name")
            longrepr = tc.get("longrepr") or ""
            msg = longrepr.splitlines()[0] if longrepr else ""
            failures.append((nodeid, msg))

    if failures:
        lines.append("### Failure details (first 10)")
        for name, msg in failures[:10]:
            lines.append(f'- `{name}`: {msg or "no message"}')

    return "\n".join(lines)


def post_comment(body, token, repo, pr_number, api_url=None):
    api_url = api_url or "https://api.github.com"
    url = f"{api_url}/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    resp = requests.post(url, headers=headers, json={"body": body})
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        print("Failed to post comment:", resp.status_code)
        print(resp.text)
        return None
    print("Comment posted:", resp.status_code)
    return resp.json()


def main():
    data = load_report()
    if not data:
        print("report.json not found, skipping comment")
        return 0

    body = build_body(data)
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("REPO")
    pr = os.environ.get("PR_NUMBER")
    api = os.environ.get("GITHUB_API_URL")
    if not token or not repo or not pr:
        print("Missing GITHUB_TOKEN, REPO or PR_NUMBER environment variables")
        return 2

    post_comment(body, token, repo, pr, api)
    return 0


if __name__ == "__main__":
    sys.exit(main())
