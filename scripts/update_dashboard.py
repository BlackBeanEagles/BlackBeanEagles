#!/usr/bin/env python3
"""Refresh live dashboard markers in the profile README from GitHub API data."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

QUOTES = [
    "The best error message is the one that never appears.",
    "Security is not a product — it is a process.",
    "First solve the problem. Then write the code.",
    "Good commits tell a story. Great commits tell the truth.",
    "AI amplifies intent. Clear intent amplifies impact.",
    "Ship small. Ship often. Ship securely.",
    "Make it work, make it right, make it fast — in that order.",
]


def api_get(path: str) -> object:
    token = os.environ.get("GH_TOKEN", "")
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "BlackBeanEagles-profile-dashboard",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def format_event(event: dict) -> str:
    repo_name = event.get("repo", {}).get("name", "unknown").split("/")[-1]
    event_type = event.get("type", "Activity")

    if event_type == "PushEvent":
        return f"push -> {repo_name}"
    if event_type == "CreateEvent":
        return f"created -> {repo_name}"
    if event_type == "PullRequestEvent":
        return f"PR -> {repo_name}"
    return f"{event_type.replace('Event', '')} -> {repo_name}"


def replace_section(content: str, marker: str, replacement: str) -> str:
    pattern = re.compile(
        rf"<!-- {marker}:START -->.*?<!-- {marker}:END -->",
        re.DOTALL,
    )
    return pattern.sub(replacement, content)


def main() -> int:
    username = os.environ.get("USERNAME", "BlackBeanEagles")
    profile = api_get(f"/users/{username}")
    repos = api_get(f"/users/{username}/repos?sort=pushed&direction=desc&per_page=10")
    events = api_get(f"/users/{username}/events/public?per_page=1")

    filtered_repos = [repo for repo in repos if repo.get("name") != "BlackBeanEagles"]
    if not filtered_repos:
        print("No repositories found to display.", file=sys.stderr)
        return 1

    latest = filtered_repos[0]
    name = latest["name"]
    url = latest["html_url"]
    lang = latest.get("language") or "Multi"
    pushed = latest.get("pushed_at", "")[:10]

    recent_lines = []
    for repo in filtered_repos[:6]:
        repo_lang = repo.get("language") or "Multi"
        repo_date = repo.get("pushed_at", "")[:10]
        recent_lines.append(
            f"- [{repo['name']}]({repo['html_url']}) — {repo_lang} · {repo_date}"
        )

    last_event = format_event(events[0]) if events else "quiet mode"
    dev_quote = QUOTES[int(datetime.now(timezone.utc).strftime("%j")) % len(QUOTES)]

    sections = {
        "NOW_BUILDING": f"""<!-- NOW_BUILDING:START -->
> **Now building:** [`{name}`]({url}) · `{lang}` · last push `{pushed}`

```bash
$ git clone {url}.git && cd {name} && echo "Let's build."
```
<!-- NOW_BUILDING:END -->""",
        "LIVE_FEED": f"""<!-- LIVE_FEED:START -->
| Signal | Value |
| :--- | :--- |
| **Last public activity** | `{last_event}` |
| **Public repos** | `{profile.get('public_repos', 0)}` |
| **Followers** | `{profile.get('followers', 0)}` |
| **Profile sync** | auto-updated every 6 hours |
<!-- LIVE_FEED:END -->""",
        "RECENT_REPOS": "<!-- RECENT_REPOS:START -->\n"
        + "\n".join(recent_lines)
        + "\n<!-- RECENT_REPOS:END -->",
        "DEV_QUOTE": f"""<!-- DEV_QUOTE:START -->
> *"{dev_quote}"*
<!-- DEV_QUOTE:END -->""",
    }

    with open("README.md", "r", encoding="utf-8") as handle:
        content = handle.read()

    for marker, replacement in sections.items():
        content = replace_section(content, marker, replacement)

    with open("README.md", "w", encoding="utf-8") as handle:
        handle.write(content)

    print(f"Updated dashboard for {username}: now building {name}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as error:
        print(f"GitHub API error: {error.code} {error.reason}", file=sys.stderr)
        raise SystemExit(1)
