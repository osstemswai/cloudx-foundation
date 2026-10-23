#!/usr/bin/env python3
"""cloudXDS 저장소의 `Icon/`을 이 저장소로 복사하고 생성물(아이콘 · 토큰 · 페이지)을 다시 만듭니다.

    python3 tools/sync.py <cloudXDS 경로>

복사  Icon/svg/<카테고리>/*.svg            → svg/<카테고리>/
      Icon/_sets.json · _ink.json · _keywords.json → meta/
기록  meta/source.json (원본 저장소 · 커밋 · 날짜 · 개수)
빌드  tools/build-tokens.py → tools/build-sprite.py → tools/build-gallery.py → tools/build-foundation.py

토큰(tokens/*.json)은 여기서 복사하지 않습니다 — Figma에서 Plugin API로 읽어 넣는 별도 절차입니다(README 「갱신」).

이 저장소는 복제본입니다. 아이콘을 고칠 일이 있으면 Figma(poc-Icon) → cloudXDS 순서로 고치고
여기서는 이 스크립트만 다시 돌립니다.
"""
import os, sys, json, shutil, subprocess, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
META_FILES = ("_sets.json", "_ink.json", "_keywords.json")


def git(src, *args):
    try:
        return subprocess.check_output(["git", "-C", src] + list(args), stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = os.path.abspath(sys.argv[1])
    icon = os.path.join(src, "Icon")
    if not os.path.isdir(os.path.join(icon, "svg")):
        sys.exit("Icon/svg 가 없습니다: %s" % icon)

    # 1. 낱개 SVG — 카테고리 폴더만 복사한다 (_index.json 같은 보고서는 두지 않는다)
    dst = os.path.join(ROOT, "svg")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    n, cats = 0, {}
    for cat in sorted(os.listdir(os.path.join(icon, "svg"))):
        d = os.path.join(icon, "svg", cat)
        if not os.path.isdir(d):
            continue
        os.makedirs(os.path.join(dst, cat))
        k = 0
        for f in sorted(os.listdir(d)):
            if f.endswith(".svg"):
                shutil.copy2(os.path.join(d, f), os.path.join(dst, cat, f))
                k += 1
        cats[cat] = k
        n += k

    # 2. 메타 — 세트 순서 · 그림 크기 · 한국어 키워드
    meta = os.path.join(ROOT, "meta")
    os.makedirs(meta, exist_ok=True)
    for f in META_FILES:
        p = os.path.join(icon, f)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(meta, f))

    # 3. 출처 스탬프
    dirty = bool(git(src, "status", "--porcelain", "--", "Icon"))
    stamp = {
        "repo": git(src, "remote", "get-url", "origin") or src,
        "commit": git(src, "rev-parse", "--short", "HEAD"),
        "commit_date": git(src, "log", "-1", "--format=%cs", "--", "Icon"),
        "dirty": dirty,
        "synced": datetime.date.today().isoformat(),
        "figma": {"library": "OnePlatform-Icon (구 poc-Icon)", "file": "iQOmpWb3Ze2M1pzfa8bvkG", "page": "icon", "node": "2806:36607"},
        "count": n,
        "categories": cats,
    }
    with open(os.path.join(meta, "source.json"), "w", encoding="utf-8") as fp:
        json.dump(stamp, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    print("복사 — 아이콘 %d개 · 카테고리 %d · 원본 %s%s" % (n, len(cats), stamp["commit"], " (작업 트리 변경 있음)" if dirty else ""), file=sys.stderr)

    # 4. 빌드
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call([sys.executable, os.path.join(here, "build-tokens.py")])
    subprocess.check_call([sys.executable, os.path.join(here, "build-sprite.py")])
    subprocess.check_call([sys.executable, os.path.join(here, "build-gallery.py")])
    subprocess.check_call([sys.executable, os.path.join(here, "build-foundation.py")])


if __name__ == "__main__":
    main()
