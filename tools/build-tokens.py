#!/usr/bin/env python3
"""tokens/*.json (Figma 변수 덤프) → tokens.css · tokens.json

    python3 tools/build-tokens.py

공유 대상은 primitive(컬러 팔레트 · 수치 스케일) · typography(글자 원자) 두 층입니다. semantic(역할 토큰)과 component 는
이후에 공유하기로 해서 `tokens/*.json`에만 두고 CSS·다운로드에는 넣지 않습니다(2026-10-23 결정).

이름 규칙 — Figma의 `/`를 `-`로 바꿉니다(cloudXDS tokens.css와 같은 규칙).
  color/bg/brand/strong/default  →  --color-bg-brand-strong-default
별칭은 primitive까지 풀어 실제 값(hex · px)으로 냅니다. `{"color": <별칭>, "opacity": 30}` 형태는 알파를 곱합니다(퍼센트).
"""
import json, os, sys, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TOK = os.path.join(ROOT, "tokens")
FILES = ["primitive", "semantic", "component", "typography"]
LAYERS = [("primitive", "primitive — 팔레트·스케일"), ("typography", "typography — 글자 원자")]   # semantic · component 는 이후 공유
FONT_WEIGHT = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}


def load():
    """(collection, name) -> var. 컬렉션 이름은 JSON 안의 선언을 따릅니다."""
    byname, sources = {}, {}
    for f in FILES:
        p = os.path.join(TOK, f + ".json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        c = d["source"]["collection"]["name"].replace("(published)", "")
        sources[c] = d["source"]
        for v in d["variables"]:
            byname[(c, v["name"])] = v
    return byname, sources


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def as_rgba(value, alpha):
    if isinstance(value, str) and value.startswith("#") and len(value) == 7:
        return "rgba(%d, %d, %d, %s)" % (*hex_to_rgb(value), round(alpha, 3))
    return "%s (a=%s)" % (value, round(alpha, 3))


def fmt_color(raw):
    if not isinstance(raw, dict):
        return raw
    c = raw.get("color", raw)
    a = c.get("a", 1)
    if abs(a - 1) < 1e-6:
        return raw.get("hex", "")[:7] or "#%02X%02X%02X" % tuple(round(c.get(k, 0) * 255) for k in "rgb")
    return "rgba(%d, %d, %d, %s)" % (*(round(c.get(k, 0) * 255) for k in "rgb"), round(a, 3))


def fmt_num(val):
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def resolve(byname, collection, name, mode=None, _seen=None):
    """반환: (값, [체인 'collection:name' …])"""
    _seen = _seen or set()
    key = (collection, name)
    if key in _seen:
        return ("<순환참조>", [])
    _seen.add(key)
    v = byname.get(key)
    if v is None:
        return ("<없음: %s/%s>" % (collection, name), [])
    vals = v["valuesByMode"]
    m = mode if mode in vals else next(iter(vals))
    raw = vals[m]
    if isinstance(raw, dict) and isinstance(raw.get("color"), dict) and raw["color"].get("type") == "VARIABLE_ALIAS":
        inner = raw["color"]
        val, chain = resolve(byname, inner["collection"], inner["name"], mode, _seen)
        op = raw.get("opacity", 100) / 100.0
        return (val if abs(op - 1) < 1e-6 else as_rgba(val, op), ["%s:%s" % (inner["collection"], inner["name"])] + chain)
    if isinstance(raw, dict) and raw.get("type") == "VARIABLE_ALIAS":
        if not raw.get("name"):
            return ("<없음: 원격 %s>" % raw.get("id"), [])
        val, chain = resolve(byname, raw["collection"], raw["name"], mode, _seen)
        return (val, ["%s:%s" % (raw["collection"], raw["name"])] + chain)
    if v["resolvedType"] == "COLOR":
        return (fmt_color(raw), [])
    return (fmt_num(raw), [])


def css_name(name):
    return "--" + name.replace("/", "-").replace(".", "-")


def css_value(name, val):
    """(값 문자열, 단위 없는 숫자인지)"""
    if name.startswith("font-weight/"):
        return str(FONT_WEIGHT.get(str(val).lower(), val))
    if name.startswith("font-family/"):
        return '"%s", sans-serif' % val
    if isinstance(val, (int, float)):
        return "%spx" % val
    return str(val)


def build():
    byname, sources = load()
    stamp = sources.get("primitive", {})
    css = ["/* Cloud X Foundation 토큰 — tools/build-tokens.py 생성물. 직접 고치지 않습니다.",
           "   원본: Figma %s · %s 기준 · 이름의 `/`는 `-`로 바꿨습니다. */" % (stamp.get("fileKey", "?"), stamp.get("exportedAt", "?")),
           ":root {"]
    data = {"source": {"figmaFile": stamp.get("fileKey"), "exportedAt": stamp.get("exportedAt"), "generatedBy": "tools/build-tokens.py"},
            "layers": {}, "textStyles": [], "effectStyles": []}
    missing = []
    for layer, label in LAYERS:
        names = sorted(n for (c, n) in byname if c == layer)
        css.append("\n  /* ── %s (%d) ── */" % (label, len(names)))
        rows = []
        for n in names:
            v = byname[(layer, n)]
            val, chain = resolve(byname, layer, n)
            if isinstance(val, str) and val.startswith("<"):
                missing.append("%s/%s → %s" % (layer, n, val))
                css.append("  /* %s: 미해결 %s */" % (css_name(n), val))
                continue
            cv = css_value(n, val)
            css.append("  %s: %s;" % (css_name(n), cv))
            rows.append({"name": n, "type": v["resolvedType"], "value": val, "css": cv, "cssVar": css_name(n),
                         "alias": chain[0].split(":", 1)[1] if chain else None, "chain": chain,
                         "scopes": v.get("scopes", []), "description": v.get("description", ""), "key": v.get("key")})
        data["layers"][layer] = rows
    css.append("}")
    sp = os.path.join(TOK, "styles.json")
    if os.path.exists(sp):
        st = json.load(open(sp, encoding="utf-8"))
        for s in st.get("textStyles", []):
            lh = s.get("lineHeight") or {}
            ls = s.get("letterSpacing") or {}
            data["textStyles"].append({
                "name": s["name"], "family": s["fontName"]["family"], "style": s["fontName"]["style"],
                "weight": FONT_WEIGHT.get(s["fontName"]["style"].replace(" ", "").lower(), s["fontName"]["style"]),
                "size": s["fontSize"], "lineHeight": lh.get("value") if lh.get("unit") == "PIXELS" else lh.get("unit"),
                "letterSpacing": ls.get("value", 0) if ls.get("unit") == "PIXELS" else 0,
                "css": "font: %s %spx/%spx \"%s\", sans-serif;" % (FONT_WEIGHT.get(s["fontName"]["style"].replace(" ", "").lower(), 400), s["fontSize"],
                                                                lh.get("value", s["fontSize"]), s["fontName"]["family"]),
                "boundVariables": {k: (b.get("name") if isinstance(b, dict) else b) for k, b in (s.get("boundVariables") or {}).items()},
                "description": s.get("description", ""), "key": s.get("key")})
        for e in st.get("effectStyles", []):
            data["effectStyles"].append({"name": e["name"], "description": e.get("description", ""), "effects": e.get("effects", []), "key": e.get("key")})
    with open(os.path.join(ROOT, "tokens.css"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(css) + "\n")
    with open(os.path.join(ROOT, "tokens.json"), "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    counts = {k: len(v) for k, v in data["layers"].items()}
    print("tokens.css · tokens.json — %s · 텍스트 스타일 %d · 이펙트 %d%s" % (
        " · ".join("%s %d" % kv for kv in counts.items()), len(data["textStyles"]), len(data["effectStyles"]),
        (" · 미해결 %d" % len(missing)) if missing else ""), file=sys.stderr)
    for m in missing:
        print("  미해결: " + m, file=sys.stderr)
    return data


if __name__ == "__main__":
    build()
