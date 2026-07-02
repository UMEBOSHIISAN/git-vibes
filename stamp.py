#!/usr/bin/env python3
"""git-vibes stamp — commitのたびにランダムなドット絵を表示する、ちょっとした儀式。

pre-commitフックから呼ばれる想定。何もチェックしない・コミットを止めない・失敗しても exit 0。
"""
import random
import sys

RESET = "\033[0m"
BLOCK = "██"


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


STAMPS = {
    "invader": {
        "rows": [
            "..XX..XX..",
            "...XXXX...",
            ".XXXXXXXX.",
            "X.XXXXXX.X",
            ".X.XX.XX.X",
            "..XXXXXX..",
            ".X......X.",
        ],
        "color": (253, 138, 46),
    },
    "ufo": {
        "rows": [
            "...DDDD...",
            "..DDDDDD..",
            ".SSSSSSSS.",
            "OOOOOOOOOO",
            "..L..L..L.",
        ],
        "color": (110, 143, 224),
    },
    "heart": {
        "rows": [
            ".XX.XX.",
            "XXXXXXX",
            "XXXXXXX",
            ".XXXXX.",
            "..XXX..",
            "...X...",
        ],
        "color": (219, 66, 133),
    },
    "star": {
        "rows": [
            "...X...",
            "...X...",
            "X..X..X",
            ".XXXXX.",
            "X..X..X",
            "...X...",
            "...X...",
        ],
        "color": (255, 220, 80),
    },
    "rocket": {
        "rows": [
            "..X..",
            ".XXX.",
            ".XXX.",
            "XXXXX",
            "XXXXX",
            "XXXXX",
            "X.X.X",
            "X...X",
            ".X.X.",
        ],
        "color": (100, 200, 230),
    },
    "mushroom": {
        "rows": [
            "..XXX..",
            ".XXXXX.",
            "XXXXXXX",
            "..XXX..",
            "..XXX..",
            ".XX.XX.",
        ],
        "color": (220, 90, 90),
    },
}

RARE_COLOR = (255, 210, 77)
RARE_CHANCE = 0.08


def render(stamp, rare=False):
    color = RARE_COLOR if rare else stamp["color"]
    lines = []
    for row in stamp["rows"]:
        line = ""
        for ch in row:
            if ch == "." or ch == " ":
                line += "  "
            else:
                line += rgb(*color) + BLOCK + RESET
        lines.append(line)
    return "\n".join(lines)


def main():
    name = random.choice(list(STAMPS.keys()))
    rare = random.random() < RARE_CHANCE
    stamp = STAMPS[name]

    print()
    print(render(stamp, rare))
    label = f"✨ rare {name}!" if rare else name
    print(f"  {label}")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
