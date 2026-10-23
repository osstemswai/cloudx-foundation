#!/usr/bin/env python3
"""절들을 모아 index.html 한 장을 만듭니다 — 왼쪽 LNB · `#c-Icon` 식 해시 전환 (스토리북과 같은 구조).

    python3 tools/build-site.py        # 먼저 build-tokens.py · build-sprite.py · build-gallery.py

순서: 안내(시작하기) → 파운데이션(Icon · Color · Number · Typography)
"""
import os, sys, json, importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import page


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    gallery = load("build-gallery")
    foundation = load("build-foundation")
    d = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf-8"))
    stamp = d["source"].get("exportedAt") or ""
    sprite = open(os.path.join(ROOT, "sprite.svg"), encoding="utf-8").read()
    source = json.load(open(os.path.join(ROOT, "meta", "source.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "meta", "source.json")) else {}
    cats = gallery.collect()
    icon_sec, nicons, nsets = gallery.section(cats, source, sprite)
    secs = foundation.sections(d, stamp, nicons)
    order = [secs[0], icon_sec] + secs[1:]
    ntok = sum(len(v) for v in d["layers"].values())
    html = page.render_app(order, stamp=stamp, counts="아이콘 %d · 토큰 %d · 텍스트 스타일 %d" % (nicons, ntok, len(d["textStyles"])))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(html)
    print("index.html — 절 %d개 (%s) · %.0fKB" % (len(order), " · ".join(s["id"] for s in order), len(html) / 1024), file=sys.stderr)


if __name__ == "__main__":
    main()
