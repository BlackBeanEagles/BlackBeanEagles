#!/usr/bin/env python3
"""Generate full-width sideways celebration SVG for the profile README."""

from __future__ import annotations

from pathlib import Path

W, H = 1600, 280
COLORS = ["#06B6D4", "#7C3AED", "#EC4899", "#F59E0B", "#22C55E", "#E879F9"]
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "welcome-confetti.svg"
PARADE_OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "celebration-parade.svg"


def particle_from_left(index: int) -> list[str]:
    y = 18 + (index * 9) % 240
    color = COLORS[index % len(COLORS)]
    duration = 2.2 + (index % 7) * 0.25
    begin = (index % 10) * 0.18
    end_x = 500 + (index * 37) % 900
    shape = index % 3

    if shape == 0:
        return [
            f'  <rect x="-80" y="{y}" width="10" height="16" fill="{color}" rx="2">',
            f'    <animate attributeName="x" values="-120;{end_x};{end_x + 80}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="y" values="{y - 8};{y + 6};{y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </rect>",
        ]

    if shape == 1:
        return [
            f'  <circle cy="{y}" r="6" fill="{color}">',
            f'    <animate attributeName="cx" values="-60;{end_x};{end_x + 100}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="cy" values="{y - 12};{y + 10};{y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;1;0.6;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </circle>",
        ]

    return [
        f'  <polygon fill="{color}" points="0,0 6,0 3,10" transform="translate(-80 {y})">',
        f'    <animateTransform attributeName="transform" type="translate" values="-120 {y}; {end_x} {y + 4}; {end_x + 120} {y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        f'    <animate attributeName="opacity" values="0;1;1;0.5;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        "  </polygon>",
    ]


def particle_from_right(index: int) -> list[str]:
    y = 30 + (index * 11) % 230
    color = COLORS[(index + 2) % len(COLORS)]
    duration = 2.0 + (index % 8) * 0.22
    begin = 0.1 + (index % 9) * 0.16
    end_x = 1100 - (index * 31) % 900
    shape = (index + 1) % 3

    if shape == 0:
        return [
            f'  <rect x="1680" y="{y}" width="9" height="15" fill="{color}" rx="2">',
            f'    <animate attributeName="x" values="1720;{end_x};{end_x - 80}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="y" values="{y + 10};{y - 6};{y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </rect>",
        ]

    if shape == 1:
        return [
            f'  <circle cy="{y}" r="5" fill="{color}">',
            f'    <animate attributeName="cx" values="1660;{end_x};{end_x - 100}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="cy" values="{y + 12};{y - 8};{y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;1;0.6;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </circle>",
        ]

    return [
        f'  <polygon fill="{color}" points="0,0 8,0 4,12" transform="translate(1680 {y})">',
        f'    <animateTransform attributeName="transform" type="translate" values="1720 {y}; {end_x} {y - 4}; {end_x - 120} {y}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        f'    <animate attributeName="opacity" values="0;1;1;0.5;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        "  </polygon>",
    ]


def main() -> None:
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="280" '
        f'viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
        'role="img" aria-label="Full screen sideways celebration">',
        "  <defs>",
        '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.10"/>',
        '      <stop offset="50%" stop-color="#7C3AED" stop-opacity="0.14"/>',
        '      <stop offset="100%" stop-color="#EC4899" stop-opacity="0.10"/>',
        "    </linearGradient>",
        '    <linearGradient id="txt" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#06B6D4"/>',
        '      <stop offset="50%" stop-color="#E879F9"/>',
        '      <stop offset="100%" stop-color="#7C3AED"/>',
        "    </linearGradient>",
        "  </defs>",
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>',
    ]

    for index in range(32):
        lines.extend(particle_from_left(index))
    for index in range(32):
        lines.extend(particle_from_right(index))

    lines.extend(
        [
            '  <g transform="translate(800 130)">',
            '    <text text-anchor="middle" y="0" fill="url(#txt)" font-family="ui-monospace, monospace" font-size="34" font-weight="700">Thanks for visiting!</text>',
            '    <text text-anchor="middle" y="34" fill="#9CA3AF" font-family="ui-monospace, monospace" font-size="14">celebration sweeping in from both sides</text>',
            '    <animateTransform attributeName="transform" type="scale" additive="sum" values="1;1.05;1;0.98;1" dur="2s" repeatCount="indefinite"/>',
            "  </g>",
            '  <rect x="0" y="0" width="140" height="280" fill="#06B6D4" opacity="0.08">',
            '    <animate attributeName="x" values="-160;0;-160" dur="2.8s" repeatCount="indefinite"/>',
            "  </rect>",
            '  <rect x="1460" y="0" width="140" height="280" fill="#EC4899" opacity="0.08">',
            '    <animate attributeName="x" values="1600;1460;1600" dur="2.8s" repeatCount="indefinite"/>',
            "  </rect>",
            "</svg>",
        ]
    )

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


def generate_parade() -> None:
    icons = ["*", "+", "x", "o", ">", "<", "~", "^"]
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="90" '
        f'viewBox="0 0 {W} 90" preserveAspectRatio="xMidYMid slice" '
        'role="img" aria-label="Sideways celebration parade">',
        f'  <rect x="0" y="0" width="{W}" height="90" fill="transparent"/>',
    ]

    for index in range(20):
        y = 12 + (index * 4) % 70
        color = COLORS[index % len(COLORS)]
        icon = icons[index % len(icons)]
        duration = 1.8 + (index % 5) * 0.2
        begin = (index % 8) * 0.12
        end_x = 400 + (index * 53) % 800
        lines.extend(
            [
                f'  <g transform="translate(-80 {y - 8})">',
                f'    <text fill="{color}" font-family="ui-monospace, monospace" font-size="22" font-weight="700">{icon}</text>',
                f'    <animateTransform attributeName="transform" type="translate" values="-80 {y - 8}; {end_x} {y}; {end_x + 100} {y - 4}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
                "  </g>",
            ]
        )

    for index in range(20):
        y = 18 + (index * 4) % 65
        color = COLORS[(index + 3) % len(COLORS)]
        icon = icons[(index + 2) % len(icons)]
        duration = 1.7 + (index % 6) * 0.18
        begin = 0.08 + (index % 7) * 0.14
        end_x = 1200 - (index * 47) % 800
        lines.extend(
            [
                f'  <g transform="translate(1680 {y - 8})">',
                f'    <text fill="{color}" font-family="ui-monospace, monospace" font-size="22" font-weight="700">{icon}</text>',
                f'    <animateTransform attributeName="transform" type="translate" values="1680 {y - 8}; {end_x} {y}; {end_x - 100} {y + 4}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
                "  </g>",
            ]
        )

    lines.append("</svg>")
    PARADE_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {PARADE_OUTPUT}")


if __name__ == "__main__":
    main()
    generate_parade()
