#!/usr/bin/env python3
"""Claude Code 本体の spinner verbs と spinner-verbs.json を照合する。

    ./check-upstream.py

exit 0 = 一致 / 1 = 差分あり / 2 = バイナリが見つからない
"""
import codecs
import json
import os
import pathlib
import re
import subprocess
import sys

VERSIONS = pathlib.Path.home() / ".local/share/claude/versions"
DATA = pathlib.Path(__file__).resolve().parent / "spinner-verbs.json"


def latest_binary():
    if not VERSIONS.is_dir():
        return None
    bins = [p for p in VERSIONS.iterdir() if p.is_file() and os.access(p, os.X_OK)]
    if not bins:
        return None
    return max(bins, key=lambda p: [int(x) if x.isdigit() else 0 for x in p.name.split(".")])


def upstream_verbs(binary):
    # 動詞配列は JS の配列リテラルとして 1 行に収まっているので、先頭要素を起点に切り出す
    out = subprocess.run(
        ["grep", "-ao", r'\["Accomplishing"[^]]*\]', str(binary)],
        capture_output=True, text=True, errors="replace",
    ).stdout
    line = out.split("\n")[0]
    if not line:
        return []
    # Flambéing / Sautéing は \xE9 で埋め込まれているのでデコードが要る
    lits = re.findall(r'"((?:[^"\\]|\\.)*)"', line)
    return [codecs.decode(x.replace("\\'", "'"), "unicode_escape") for x in lits]


def ours():
    verbs = json.load(DATA.open())["spinnerVerbs"]["verbs"]
    return [v.split("(")[0] for v in verbs]


def main():
    binary = latest_binary()
    if binary is None:
        print(f"Claude Code のバイナリが見つかりません: {VERSIONS}", file=sys.stderr)
        return 2

    up, mine = upstream_verbs(binary), ours()
    if not up:
        print(f"{binary.name} から動詞配列を取り出せませんでした（本家の構造が変わった可能性）", file=sys.stderr)
        return 2

    added = [w for w in up if w not in mine]
    removed = [w for w in mine if w not in up]
    print(f"Claude Code {binary.name} と照合: 本家 {len(up)} 語 / 手元 {len(mine)} 語")

    if not added and not removed:
        print("差分なし")
        return 0
    if added:
        print(f"\n本家に増えた語 ({len(added)}):")
        for w in added:
            print(f"  + {w}")
    if removed:
        print(f"\n本家から消えた語 ({len(removed)}):")
        for w in removed:
            print(f"  - {w}")
    print("\nspinner-verbs.json を更新する")
    return 1


if __name__ == "__main__":
    sys.exit(main())
