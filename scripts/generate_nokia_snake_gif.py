#!/usr/bin/env python3
"""
generate_nokia_snake_gif.py
Builds a classic Nokia 3310-style Snake GIF: LCD grid, random food dots, snake eating them.
Output: assets/nokia-snake.gif (used by the profile README).
"""

from __future__ import annotations

import random
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "nokia-snake.gif"

# Nokia 3310 LCD palette
LCD_BG = (196, 207, 71)
LCD_CELL = (155, 188, 15)
PIXEL = (15, 56, 15)
BEZEL = (58, 58, 58)
BEZEL_HI = (96, 96, 96)
SCREEN_BG = (48, 48, 48)

CELL = 13
COLS = 53
ROWS = 7
PAD = 10
HEADER = 28
FOOTER = 18
WIDTH = COLS * CELL + PAD * 2
HEIGHT = ROWS * CELL + PAD * 2 + HEADER + FOOTER
FPS = 11
STEPS = 96
SEED = 3310


def spawn_food(snake: set[tuple[int, int]], rng: random.Random) -> tuple[int, int]:
    empty = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in snake]
    return rng.choice(empty)


def bfs_step(
    head: tuple[int, int],
    goal: tuple[int, int],
    blocked: set[tuple[int, int]],
) -> tuple[int, int] | None:
    queue: deque[tuple[tuple[int, int], tuple[int, int] | None]] = deque([(head, None)])
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {head: None}

    while queue:
        current, _ = queue.popleft()
        if current == goal:
            node = current
            while came_from[node] is not None and came_from[came_from[node]] is not None:  # type: ignore[index]
                node = came_from[node]  # type: ignore[assignment]
            return node
        cx, cy = current
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cx + dx, cy + dy)
            if (
                0 <= nxt[0] < COLS
                and 0 <= nxt[1] < ROWS
                and nxt not in came_from
                and nxt not in blocked
            ):
                came_from[nxt] = current
                queue.append((nxt, current))
    return None


def simulate() -> list[tuple[list[tuple[int, int]], tuple[int, int], bool]]:
    rng = random.Random(SEED)
    snake: list[tuple[int, int]] = [(8, ROWS // 2), (7, ROWS // 2), (6, ROWS // 2)]
    food = spawn_food(set(snake), rng)
    frames: list[tuple[list[tuple[int, int]], tuple[int, int], bool]] = []

    for tick in range(STEPS):
        head = snake[0]
        blocked = set(snake[:-1])
        nxt = bfs_step(head, food, blocked)

        if nxt is None:
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                candidate = (head[0] + dx, head[1] + dy)
                if (
                    0 <= candidate[0] < COLS
                    and 0 <= candidate[1] < ROWS
                    and candidate not in blocked
                ):
                    nxt = candidate
                    break

        if nxt is None:
            snake = [(8, ROWS // 2), (7, ROWS // 2), (6, ROWS // 2)]
            food = spawn_food(set(snake), rng)
            frames.append((snake.copy(), food, tick % 2 == 0))
            continue

        snake.insert(0, nxt)
        ate = nxt == food
        if ate:
            food = spawn_food(set(snake), rng)
        else:
            snake.pop()

        frames.append((snake.copy(), food, tick % 2 == 0))

    return frames


def draw_frame(snake: list[tuple[int, int]], food: tuple[int, int], food_visible: bool) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), SCREEN_BG)
    draw = ImageDraw.Draw(img)

    outer = (4, 4, WIDTH - 5, HEIGHT - 5)
    draw.rounded_rectangle(outer, radius=10, fill=BEZEL, outline=BEZEL_HI, width=2)

    screen = (PAD - 2, HEADER - 4, WIDTH - PAD + 1, HEIGHT - FOOTER + 2)
    draw.rounded_rectangle(screen, radius=4, fill=LCD_BG, outline=PIXEL, width=1)

    draw.text((PAD, 8), "NOKIA SNAKE", fill=(220, 220, 220))
    draw.text((WIDTH - 72, 8), "3310", fill=(170, 170, 170))

    origin_x = PAD
    origin_y = HEADER

    for row in range(ROWS):
        for col in range(COLS):
            x0 = origin_x + col * CELL
            y0 = origin_y + row * CELL
            shade = LCD_CELL if (row + col) % 2 == 0 else LCD_BG
            draw.rectangle((x0, y0, x0 + CELL - 1, y0 + CELL - 1), fill=shade)

    if food_visible:
        fx, fy = food
        x0 = origin_x + fx * CELL + 2
        y0 = origin_y + fy * CELL + 2
        draw.rectangle((x0, y0, x0 + CELL - 5, y0 + CELL - 5), fill=PIXEL)

    for i, (sx, sy) in enumerate(snake):
        x0 = origin_x + sx * CELL + 1
        y0 = origin_y + sy * CELL + 1
        inset = 2 if i == 0 else 3
        draw.rectangle(
            (x0 + inset, y0 + inset, x0 + CELL - inset - 1, y0 + CELL - inset - 1),
            fill=PIXEL,
        )

    draw.text((PAD, HEIGHT - FOOTER + 2), "SCORE", fill=(180, 180, 180))
    draw.text((WIDTH - 56, HEIGHT - FOOTER + 2), f"{max(0, len(snake) - 3):02d}", fill=(220, 220, 220))

    return img


def main() -> None:
    frames_data = simulate()
    images = [draw_frame(snake, food, blink) for snake, food, blink in frames_data]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        OUTPUT,
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / FPS),
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUTPUT} ({len(images)} frames, {OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
