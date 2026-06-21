#!/usr/bin/env python3
"""Generate valid, GitHub-safe celebration SVG assets for the profile README."""

from __future__ import annotations

import html
from pathlib import Path

W = 1200
CONFETTI_H = 200
PARADE_H = 72
COLORS = ["#FF006E", "#8338EC", "#FFBE0B", "#00F5FF", "#39FF14", "#FB5607"]
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "welcome-confetti.svg"
PARADE_OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "celebration-parade.svg"


def particle_from_left(index: int) -> list[str]:
    y = 20 + (index * 11) % 160
    color = COLORS[index % len(COLORS)]
    duration = 2.4 + (index % 5) * 0.2
    begin = (index % 8) * 0.15
    end_x = 450 + (index * 41) % 650
    shape = index % 3

    if shape == 0:
        return [
            f'  <rect x="-60" y="{y}" width="9" height="14" fill="{color}" rx="2">',
            f'    <animate attributeName="x" values="-90;{end_x};{end_x + 70}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;0.8;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </rect>",
        ]
    if shape == 1:
        return [
            f'  <circle cy="{y}" r="5" fill="{color}">',
            f'    <animate attributeName="cx" values="-40;{end_x};{end_x + 80}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </circle>",
        ]
    return [
        f'  <rect x="-60" y="{y}" width="8" height="8" fill="{color}" transform="rotate(45 -56 {y + 4})">',
        f'    <animate attributeName="x" values="-90;{end_x};{end_x + 70}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        f'    <animate attributeName="opacity" values="0;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        "  </rect>",
    ]


def particle_from_right(index: int) -> list[str]:
    y = 28 + (index * 13) % 150
    color = COLORS[(index + 2) % len(COLORS)]
    duration = 2.2 + (index % 6) * 0.18
    begin = 0.1 + (index % 7) * 0.14
    end_x = 950 - (index * 37) % 650
    shape = (index + 1) % 3

    if shape == 0:
        return [
            f'  <rect x="1260" y="{y}" width="9" height="14" fill="{color}" rx="2">',
            f'    <animate attributeName="x" values="1290;{end_x};{end_x - 70}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;0.8;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </rect>",
        ]
    if shape == 1:
        return [
            f'  <circle cy="{y}" r="5" fill="{color}">',
            f'    <animate attributeName="cx" values="1240;{end_x};{end_x - 80}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            f'    <animate attributeName="opacity" values="0;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
            "  </circle>",
        ]
    return [
        f'  <rect x="1260" y="{y}" width="8" height="8" fill="{color}" transform="rotate(45 1264 {y + 4})">',
        f'    <animate attributeName="x" values="1290;{end_x};{end_x - 70}" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        f'    <animate attributeName="opacity" values="0;1;0.7;0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
        "  </rect>",
    ]


def generate_confetti() -> None:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{CONFETTI_H}" viewBox="0 0 {W} {CONFETTI_H}" role="img" aria-label="Sideways celebration confetti">',
        "  <defs>",
        '    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#FF006E" stop-opacity="0.15"/>',
        '      <stop offset="50%" stop-color="#8338EC" stop-opacity="0.18"/>',
        '      <stop offset="100%" stop-color="#FFBE0B" stop-opacity="0.15"/>',
        "    </linearGradient>",
        "  </defs>",
        f'  <rect width="{W}" height="{CONFETTI_H}" fill="url(#bg)" rx="12"/>',
    ]

    for index in range(18):
        lines.extend(particle_from_left(index))
    for index in range(18):
        lines.extend(particle_from_right(index))

    lines.extend(
        [
            f'  <text x="{W // 2}" y="95" text-anchor="middle" fill="#FFFFFF" font-family="monospace" font-size="28" font-weight="700">Thanks for visiting!</text>',
            f'  <text x="{W // 2}" y="122" text-anchor="middle" fill="#FFBE0B" font-family="monospace" font-size="14">celebration sweeping in from both sides</text>',
            "</svg>",
        ]
    )
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


def generate_parade() -> None:
    icons = ["*", "#", "+", "x", "o", ">", "<", "~"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{PARADE_H}" viewBox="0 0 {W} {PARADE_H}" role="img" aria-label="Sideways celebration parade">',
        f'  <rect width="{W}" height="{PARADE_H}" fill="#0D0221" rx="10"/>',
    ]

    for index in range(14):
        y = 16 + (index * 3) % 40
        color = COLORS[index % len(COLORS)]
        icon = html.escape(icons[index % len(icons)])
        duration = 1.9 + (index % 4) * 0.15
        begin = (index % 6) * 0.1
        end_x = 350 + (index * 47) % 700
        lines.extend(
            [
                "  <g>",
                f'    <text y="{y}" fill="{color}" font-family="monospace" font-size="20" font-weight="700">{icon}</text>',
                f'    <animateTransform attributeName="transform" type="translate" values="-120 0; {end_x} 0; {end_x + 120} 0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
                "  </g>",
            ]
        )

    for index in range(14):
        y = 22 + (index * 3) % 38
        color = COLORS[(index + 3) % len(COLORS)]
        icon = html.escape(icons[(index + 2) % len(icons)])
        duration = 1.8 + (index % 5) * 0.12
        begin = 0.08 + (index % 5) * 0.12
        end_x = 850 - (index * 43) % 700
        lines.extend(
            [
                "  <g>",
                f'    <text y="{y}" fill="{color}" font-family="monospace" font-size="20" font-weight="700">{icon}</text>',
                f'    <animateTransform attributeName="transform" type="translate" values="{W + 120} 0; {end_x} 0; {end_x - 120} 0" dur="{duration}s" begin="{begin}s" repeatCount="indefinite"/>',
                "  </g>",
            ]
        )

    lines.append("</svg>")
    PARADE_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {PARADE_OUTPUT}")


def main() -> None:
    generate_confetti()
    generate_parade()


if __name__ == "__main__":
    main()
