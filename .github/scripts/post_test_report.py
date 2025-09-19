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


def load_coverage_report(path="coverage_report.txt"):
    p = Path(path)
    if not p.exists():
        return None
    return p.read_text()


def build_body(data, coverage_data=None):
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

    # Add coverage information if available
    if coverage_data:
        lines.append("## Coverage Report")
        lines.append("")

        # Extract the coverage table
        coverage_table = []
        in_coverage_table = False

        for line in coverage_data.splitlines():
            # Look for start of coverage table (line with "Name" and "Stmts")
            if (
                "Name" in line
                and "Stmts" in line
                and "Miss" in line
                and "Cover" in line
            ):
                in_coverage_table = True
                coverage_table.append(line)
                continue

            # End of coverage table (line with dashes)
            if in_coverage_table and line.startswith("TOTAL"):
                coverage_table.append(line)
                # Also add the line after TOTAL that contains the dashes
                continue

            # Add lines while inside the coverage table
            if in_coverage_table and ("---" in line or "/" in line):
                coverage_table.append(line)

        # If we extracted the coverage table, add it to the report
        if coverage_table:
            lines.append("```")
            lines.extend(coverage_table)
            lines.append("```")
            lines.append("")

        # Extract the total coverage percentage if available
        total_line = next(
            (line for line in coverage_table if line.startswith("TOTAL")), None
        )
        if total_line:
            try:
                # Parse the total coverage percentage
                parts = total_line.strip().split()
                if len(parts) >= 4:
                    total_coverage = parts[-1]
                    lines.append(f"**Total coverage: {total_coverage}**")
                    lines.append("")
            except Exception as e:
                # If parsing fails, just skip this part
                print(f"Failed to parse total coverage: {e}")
                pass

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

    # Try to load coverage data
    coverage_data = load_coverage_report()
    if not coverage_data:
        print("coverage_report.txt not found, proceeding without coverage info")

    body = build_body(data, coverage_data)
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
