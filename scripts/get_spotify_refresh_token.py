#!/usr/bin/env python3
"""One-time helper to exchange a Spotify authorization code for a refresh token."""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.parse
import urllib.request

REDIRECT_URI = "http://127.0.0.1:8080/callback"
SCOPES = "user-read-currently-playing user-read-playback-state"


def main() -> int:
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    auth_code = os.environ.get("SPOTIFY_AUTH_CODE")

    if not client_id or not client_secret:
        print("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET first.", file=sys.stderr)
        return 1

    if not auth_code:
        params = urllib.parse.urlencode(
            {
                "client_id": client_id,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "scope": SCOPES,
            }
        )
        print("Open this URL in your browser, approve access, then copy the `code` query param:\n")
        print(f"https://accounts.spotify.com/authorize?{params}\n")
        print("Then run:")
        print('  set SPOTIFY_AUTH_CODE=your_code')
        print("  python scripts/get_spotify_refresh_token.py")
        return 0

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
        }
    ).encode()

    request = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=body,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode())

    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        print(json.dumps(payload, indent=2))
        print("\nNo refresh token returned.", file=sys.stderr)
        return 1

    print("Save this as the GitHub secret SPOTIFY_REFRESH_TOKEN:\n")
    print(refresh_token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
