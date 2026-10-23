#!/usr/bin/env python3
"""svg/<카테고리>/<이름>.svg → sprite.svg (symbol 묶음).

    python3 tools/build-sprite.py

symbol id는 `i-<카테고리>-<이름>`입니다. cloudXDS의 `Icon/sprite.svg`와 같은 규칙이라
어느 쪽 스프라이트를 쓰든 참조 코드가 같습니다.

    <svg class="icon"><use href="sprite.svg#i-00_general-search"/></svg>
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "svg")
OUT = os.path.join(ROOT, "sprite.svg")


def symbols():
    for cat in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, cat)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".svg"):
                continue
            raw = open(os.path.join(d, f), encoding="utf-8").read()
            body = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
            body = re.sub(r"</svg>\s*$", "", body).strip()
            yield cat, f[:-4], body


def build():
    # 루트를 display:none 으로 숨기면 Chrome이 그 안의 <mask>·<clipPath> 참조를 버린다(excel·pin 등이 덩어리로 나옴).
    # 크기 0 + absolute 로 숨긴다. 인라인할 때도 이 루트를 그대로 둔다 (2026-10-23).
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true" focusable="false">']
    n = 0
    for cat, name, body in symbols():
        parts.append('<symbol id="i-%s-%s" viewBox="0 0 20 20" fill="none">%s</symbol>' % (cat, name, body))
        n += 1
    parts.append("</svg>")
    return "\n".join(parts), n


def main():
    out, n = build()
    open(OUT, "w", encoding="utf-8").write(out)
    print("sprite.svg — 아이콘 %d개 · %.1fKB" % (n, len(out) / 1024), file=sys.stderr)


if __name__ == "__main__":
    main()
