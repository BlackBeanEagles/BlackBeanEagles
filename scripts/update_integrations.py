#!/usr/bin/env python3
"""Update Spotify now playing and WakaTime stats sections in the profile README."""

from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

README_PATH = "README.md"


def replace_section(content: str, marker: str, replacement: str) -> str:
    pattern = re.compile(
        rf"<!-- {marker}:START -->.*?<!-- {marker}:END -->",
        re.DOTALL,
    )
    return pattern.sub(replacement, content)


def http_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        data=data,
        headers=headers or {},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def get_spotify_access_token() -> str | None:
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        return None

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    ).encode()

    status, payload = http_request(
        "https://accounts.spotify.com/api/token",
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=body,
    )

    if status != 200:
        print(f"Spotify token refresh failed: {status}", file=sys.stderr)
        return None

    return json.loads(payload.decode()).get("access_token")


def build_spotify_section() -> str:
    access_token = get_spotify_access_token()

    if not access_token:
        return """<!-- SPOTIFY_NOW_PLAYING:START -->
<table>
<tr>
<td width="72">
<img src="https://img.shields.io/badge/Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Spotify"/>
</td>
<td>

**Now playing** · awaiting connection

Add repo secrets `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REFRESH_TOKEN` to go live.

</td>
</tr>
</table>
<!-- SPOTIFY_NOW_PLAYING:END -->"""

    status, payload = http_request(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if status == 204 or not payload:
        return """<!-- SPOTIFY_NOW_PLAYING:START -->
<table>
<tr>
<td width="72">
<img src="https://img.shields.io/badge/Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Spotify"/>
</td>
<td>

**Now playing:** *Nothing playing right now* — probably deep in code.

</td>
</tr>
</table>
<!-- SPOTIFY_NOW_PLAYING:END -->"""

    if status != 200:
        print(f"Spotify now playing request failed: {status}", file=sys.stderr)
        return """<!-- SPOTIFY_NOW_PLAYING:START -->
**Spotify:** temporarily unavailable — check again soon.
<!-- SPOTIFY_NOW_PLAYING:END -->"""

    data = json.loads(payload.decode())
    item = data.get("item") or {}
    track = item.get("name", "Unknown track")
    artists = ", ".join(artist.get("name", "") for artist in item.get("artists", []))
    album = item.get("album", {}).get("name", "Unknown album")
    url = item.get("external_urls", {}).get("spotify", "https://open.spotify.com")
    images = item.get("album", {}).get("images", [])
    art_url = images[0]["url"] if images else ""
    is_playing = data.get("is_playing", False)
    status_label = "Listening now" if is_playing else "Paused on"

    art_cell = (
        f'<img src="{art_url}" width="72" height="72" alt="Album art"/>'
        if art_url
        else '<img src="https://img.shields.io/badge/Album-art-1DB954?style=flat-square" alt="Album art"/>'
    )

    return f"""<!-- SPOTIFY_NOW_PLAYING:START -->
<table>
<tr>
<td width="84" align="center">{art_cell}</td>
<td>

**{status_label}:** [{track}]({url})

`{artists}` · *{album}*

</td>
</tr>
</table>
<!-- SPOTIFY_NOW_PLAYING:END -->"""


def build_wakatime_section() -> str:
    api_key = os.environ.get("WAKATIME_API_KEY")
    username = os.environ.get("WAKATIME_USERNAME", "current")

    if not api_key:
        return """<!-- WAKATIME_STATS:START -->
| This week | Status |
| :--- | :--- |
| **Coding time** | Connect WakaTime to go live |
| **Setup** | Add `WAKATIME_API_KEY` in repo secrets |

[Get your API key](https://wakatime.com/settings/api-key)
<!-- WAKATIME_STATS:END -->"""

    auth = base64.b64encode(f"{api_key}:".encode()).decode()
    status, payload = http_request(
        f"https://wakatime.com/api/v1/users/{username}/stats/last_7_days",
        headers={"Authorization": f"Basic {auth}"},
    )

    if status != 200:
        print(f"WakaTime request failed: {status}", file=sys.stderr)
        return """<!-- WAKATIME_STATS:START -->
**WakaTime:** unable to fetch stats right now.
<!-- WAKATIME_STATS:END -->"""

    data = json.loads(payload.decode()).get("data", {})
    total = data.get("human_readable_total", "0 secs")
    daily_avg = data.get("human_readable_daily_average", "0 secs")
    languages = data.get("languages", [])[:5]
    projects = data.get("projects", [])[:3]

    lang_lines = []
    for language in languages:
        name = language.get("name", "Unknown")
        percent = language.get("percent", 0)
        text = language.get("text", "")
        lang_lines.append(f"- `{name}` · {percent:.1f}% · {text}")

    project_lines = []
    for project in projects:
        name = project.get("name", "Unknown")
        text = project.get("text", "")
        project_lines.append(f"- **{name}** · {text}")

    lang_block = "\n".join(lang_lines) if lang_lines else "- No language data yet"
    project_block = "\n".join(project_lines) if project_lines else "- No project data yet"

    return f"""<!-- WAKATIME_STATS:START -->
| Metric | Value |
| :--- | :--- |
| **Last 7 days** | `{total}` |
| **Daily average** | `{daily_avg}` |

**Top languages**

{lang_block}

**Top projects**

{project_block}
<!-- WAKATIME_STATS:END -->"""


def main() -> int:
    with open(README_PATH, "r", encoding="utf-8") as handle:
        content = handle.read()

    content = replace_section(content, "SPOTIFY_NOW_PLAYING", build_spotify_section())
    content = replace_section(content, "WAKATIME_STATS", build_wakatime_section())

    with open(README_PATH, "w", encoding="utf-8") as handle:
        handle.write(content)

    print("Updated Spotify and WakaTime profile sections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
