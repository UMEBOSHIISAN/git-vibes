#!/usr/bin/env python3
"""git-vibes fortune — 直近7日のgit logから「今週の開発運勢」を占う。

決定論的: 同じ週に何度実行しても同じラッキーアイテム/カラーになる（週番号でシード）。
コミット数の"評価"はあくまで娯楽。生産性の指標として使わない。
"""
import hashlib
import subprocess
import sys
from datetime import datetime


def get_commits(days=7):
    since = f"{days}.days.ago"
    out = subprocess.run(
        ["git", "log", f"--since={since}", "--pretty=format:%H|%ad|%s", "--date=iso-strict"],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        return []
    commits = []
    for line in out.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "date": parts[1], "msg": parts[2]})
    return commits


def analyze(commits):
    n = len(commits)
    late_night = 0
    msg_lengths = []
    for c in commits:
        try:
            dt = datetime.fromisoformat(c["date"])
            if dt.hour >= 23 or dt.hour < 5:
                late_night += 1
        except ValueError:
            pass
        msg_lengths.append(len(c["msg"]))
    avg_len = sum(msg_lengths) / len(msg_lengths) if msg_lengths else 0
    return {"n": n, "late_night": late_night, "avg_len": avg_len}


VOLUME_FORTUNES = [
    (0, "静寂の週。コードは眠り、次の一手を待っている。"),
    (5, "ゆるやかな週。小さな積み重ねが土台を作った。"),
    (15, "良いリズムの週。手が動く時ほど、休む時間も資産になる。"),
    (30, "疾走の週。勢いはあるが、コミット前に一呼吸を。"),
    (10**9, "嵐の週。何かに追われていたか、何かに火がついていたか。"),
]

LUCK_ITEMS = ["git stash", "小さいコミット", "テストを先に書く", "コーヒー", "深呼吸", "rebase前のバックアップブランチ", "早めのpush"]
LUCK_COLORS = ["緑", "青", "金", "紫", "オレンジ", "藍"]


def pick_volume_fortune(n):
    for threshold, text in VOLUME_FORTUNES:
        if n <= threshold:
            return text
    return VOLUME_FORTUNES[-1][1]


def week_seed():
    iso = datetime.now().isocalendar()
    digest = hashlib.sha256(f"{iso[0]}-W{iso[1]}".encode()).hexdigest()
    return int(digest, 16)


def main():
    commits = get_commits(7)
    stats = analyze(commits)
    seed = week_seed()

    item = LUCK_ITEMS[seed % len(LUCK_ITEMS)]
    color = LUCK_COLORS[(seed // len(LUCK_ITEMS)) % len(LUCK_COLORS)]

    print()
    print("\U0001f52e 今週の開発運勢")
    print("-" * 32)
    print(f"コミット数     : {stats['n']}")
    if stats["n"]:
        print(f"深夜コミット率  : {stats['late_night']}/{stats['n']}")
    print()
    print(pick_volume_fortune(stats["n"]))
    print()
    print(f"今週のラッキーアイテム : {item}")
    print(f"今週のラッキーカラー   : {color}")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"(fortune failed: {e})", file=sys.stderr)
    sys.exit(0)
