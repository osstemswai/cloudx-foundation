#!/usr/bin/env python3
"""tokens.json → 절(section) 4개: 시작하기 · Color · Number · Typography (build-site.py 가 index.html 로 묶는다)

    python3 tools/build-foundation.py      # 먼저 python3 tools/build-tokens.py

값은 전부 tokens.json(= Figma 변수를 primitive까지 푼 것)에서 옵니다. 문장은 여기 빌더에 있고, 수치는 손으로 적지 않습니다.
"""
import os, sys, json, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HUE_ORDER = ["neutralgray", "orange", "red", "yellow", "chartreuse", "green", "turquoise", "cyan", "blue", "purple", "pink", "black", "white"]
SEM_COLOR_GROUPS = [("bg", "bg — 바탕"), ("fg", "fg — 글자"), ("border", "border — 선"), ("icon", "icon — 아이콘"), ("focus", "focus — 포커스"), ("palette", "palette — 태그·차트 팔레트"), ("shadow", "shadow — 그림자")]
SEM_NUMBER_GROUPS = [("size", "size — 컨트롤 높이"), ("spacing", "spacing — 여백·간격"), ("radius", "radius — 모서리"), ("border", "border — 선 두께"), ("icon", "icon — 아이콘 크기"), ("focus", "focus — 포커스 링"), ("shadow", "shadow — 그림자 수치")]


def esc(s):
    return html.escape(str(s))


def num(v):
    try:
        f = float(str(v).replace("px", ""))
        return int(f) if f.is_integer() else f
    except ValueError:
        return v


def step_key(name):
    s = name.split("/")[-1]
    try:
        return (0, float(s.replace("-", ".")))
    except ValueError:
        return (1, s)


def alpha_label(v):
    """rgba(0, 0, 0, 0.1) → 'α 0.1'"""
    m = re.search(r"([\d.]+)\)$", str(v))
    return "α " + m.group(1) if m else "α"


def swatch(value):
    return '<span class="sw"><i style="background:%s"></i></span>' % esc(value)


def cp(text, label=None):
    return '<code class="cp" data-cp="%s" title="클릭하면 복사">%s</code>' % (esc(text), esc(label if label is not None else text))


# ── 역할 토큰 표 공용 조각 ───────────────────────────────────────────────
COPY_SVG = '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true"><rect x="5" y="5" width="8.5" height="8.5" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M3 10.5V3.5A1.5 1.5 0 0 1 4.5 2h6" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>'
STATES = ("default", "hover", "pressed")
PALETTE_COLS = ["bg-strong", "bg-subtle", "border", "fg", "fg-contrast"]


def tk(r, short):
    """토큰 칩. 누르면 var(--…) 복사."""
    v = "var(%s)" % r["cssVar"]
    return '<code class="tk" data-cp="%s" title="클릭: %s 복사">%s%s</code>' % (esc(v), esc(v), esc(short), COPY_SVG)


def tk_grp(label):
    return '<code class="tk tk--grp">%s</code>' % esc(label)


def prim_label(r, strip):
    a = r.get("alias")
    if not a:
        return "직접 값"
    return a[len(strip):] if a.startswith(strip) else a


def vc(r, big, small):
    """값 셀: 견본 + (굵게 primitive) + (작게 실제 값). 셀 전체가 복사 버튼."""
    v = "var(%s)" % r["cssVar"]
    sw = swatch(r["value"]) if r["type"] == "COLOR" else ""
    return '<td class="vc" data-cp="%s" title="클릭: %s 복사">%s<span class="vt"><b>%s</b><span>%s</span></span></td>' % (esc(v), esc(v), sw, esc(big), esc(small))


def vc_color(r, big=None):
    return vc(r, big if big is not None else prim_label(r, "color/"), r["value"])


def vc_number(r):
    f = num(r["value"])
    return vc(r, "full" if isinstance(f, (int, float)) and f >= 999 else "%spx" % f, prim_label(r, ""))


def vc_empty():
    return '<td class="mut">—</td>'


def rowkey(rs):
    return " ".join(" ".join([r["name"], str(r["value"]), r.get("alias") or "", r.get("description") or ""]) for r in rs).lower()


def table(widths, heads, trs, auto_min=176):
    """widths: px 또는 None(자동). 표 최소 너비 = 고정 폭 합 + 자동 열 × auto_min — 좁은 화면에선 카드 안에서 가로 스크롤."""
    cg = "".join('<col style="width:%dpx">' % w if w else "<col>" for w in widths)
    th = "".join("<th>%s</th>" % esc(h) for h in heads)
    mw = sum(w for w in widths if w) + auto_min * sum(1 for w in widths if not w)
    return '<div class="tw tw--card"><table class="t tt" style="min-width:%dpx"><colgroup>%s</colgroup><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (mw, cg, th, "".join(trs))


def color_sample(g, r):
    c = esc(r["value"]); n = r["name"]
    box = "sbox sbox--dark" if "inverted" in n else "sbox"
    if g == "fg":
        return '<span class="%s"><span class="aa" style="color:%s">Aa 가</span></span>' % (box, c)
    if g == "border":
        return '<span class="%s"><i class="bx" style="border-color:%s"></i></span>' % (box, c)
    if g == "icon":
        return '<span class="sbox"><svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true"><path d="M10 2.2l2.3 4.8 5.2.7-3.8 3.6.9 5.2L10 14l-4.6 2.5.9-5.2-3.8-3.6 5.2-.7z" fill="%s"/></svg></span>' % c
    if g == "focus":
        last = n.split("/")[-1]
        if last == "fill":
            return '<span class="sbox"><i class="fcs" style="background:%s"></i></span>' % c
        return '<span class="sbox"><i class="fcs" style="box-shadow:0 0 0 %dpx %s"></i></span>' % (2 if "outline" in last else 4, c)
    if g == "shadow":
        return '<span class="sbox sbox--pad"><i class="shd" style="box-shadow:0 2px 6px %s"></i></span>' % c
    return '<span class="sbox sbox--fill" style="background:%s"></span>' % c


def plain_color_table(g, rs):
    trs = ['<tr data-k="%s"><td class="smpc">%s</td><td>%s</td>%s</tr>' % (esc(rowkey([r])), color_sample(g, r), tk(r, r["name"][len("color/"):]), vc_color(r)) for r in rs]
    return table([100, 300, None], ["견본", "토큰", "값"], trs)


def sem_color_tables(groups, labels, gorder):
    out = []
    for g in gorder:
        rs = sorted(groups[g], key=lambda x: x["name"])
        parts = []
        if g == "bg":
            st = [r for r in rs if r["name"].split("/")[-1] in STATES]
            rest = [r for r in rs if r not in st]
            bases = {}
            for r in st:
                b, state = r["name"].rsplit("/", 1)
                bases.setdefault(b, {})[state] = r
            trs = []
            for b in sorted(bases):
                m = bases[b]
                trs.append('<tr data-k="%s"><td>%s</td>%s</tr>' % (esc(rowkey(m.values())), tk_grp(b[len("color/"):] + "/*"), "".join(vc_color(m[s]) if s in m else vc_empty() for s in STATES)))
            parts.append('<p class="tcap">상태가 있는 토큰 — 이름 끝이 default · hover · pressed 입니다. 값 칸을 누르면 그 상태의 변수가 복사됩니다.</p>' + table([220, None, None, None], ["토큰"] + list(STATES), trs))
            if rest:
                parts.append('<p class="tcap">상태가 없는 토큰</p>' + plain_color_table(g, rest))
        elif g == "palette":
            hued = [r for r in rs if r["name"].count("/") == 3]
            rest = [r for r in rs if r["name"].count("/") == 2]
            hues = {}
            for r in hued:
                _, _, h, role = r["name"].split("/")
                hues.setdefault(h, {})[role] = r
            cols = PALETTE_COLS + sorted(set(k for m in hues.values() for k in m) - set(PALETTE_COLS))
            order = [h for h in HUE_ORDER if h in hues] + sorted(h for h in hues if h not in HUE_ORDER)
            trs = []
            for h in order:
                m = hues[h]
                cells = []
                for c in cols:
                    if c not in m:
                        cells.append(vc_empty()); continue
                    a = prim_label(m[c], "color/")
                    cells.append(vc_color(m[c], a[len(h) + 1:] if a.startswith(h + "/") else a))
                trs.append('<tr data-k="%s"><td>%s</td>%s</tr>' % (esc(rowkey(m.values())), tk_grp("palette/%s/*" % h), "".join(cells)))
            parts.append('<p class="tcap">색상별 — 태그·배지·차트에 한 색을 고를 때 한 줄을 씁니다. 굵은 숫자는 그 색의 단계입니다.</p>' + table([170] + [None] * len(cols), ["토큰"] + cols, trs, auto_min=136))
            if rest:
                parts.append('<p class="tcap">색상을 정하지 않은 기본값</p>' + plain_color_table(g, rest))
        else:
            parts.append(plain_color_table(g, rs))
        out.append('<div class="sec" data-group><h4 class="sb-h4">%s<small>%d</small></h4>%s</div>' % (esc(labels.get(g, g)), len(rs), "".join(parts)))
    return "".join(out)


def sem_number_tables(groups, labels, gorder):
    out = []
    for g in gorder:
        rs = sorted(groups[g], key=lambda x: (float(num(x["value"])) if isinstance(num(x["value"]), (int, float)) else 0, x["name"]))
        trs = ['<tr data-k="%s"><td class="smpc">%s</td><td>%s</td>%s</tr>' % (esc(rowkey([r])), num_preview(g, num(r["value"]), r["name"]), tk(r, r["name"][len("number/"):]), vc_number(r)) for r in rs]
        out.append('<div class="sec" data-group><h4 class="sb-h4">%s<small>%d</small></h4>%s</div>' % (esc(labels.get(g, g)), len(rs), table([120, 300, None], ["견본", "토큰", "값"], trs)))
    return "".join(out)


SEM_TABLE_CSS = r"""
.tw--card{border:1px solid var(--line);border-radius:10px;overflow:hidden;overflow-x:auto;background:var(--card)}
.tw--card table.t{table-layout:fixed;min-width:560px}
.tw--card table.t th{background:var(--side);padding:9px 14px;font-size:12px;color:var(--ink2)}
.tw--card table.t td{padding:8px 14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tw--card table.t td.vc{overflow:visible}
.tw--card table.t tr:last-child td{border-bottom:0}
.tcap{font-size:12.5px;color:var(--ink3);margin:14px 0 6px}
.sec .tcap:first-child{margin-top:0}
.tk{display:inline-flex;align-items:center;gap:6px;max-width:100%;background:var(--chip);border:1px solid var(--line);border-radius:5px;padding:2px 7px;font-size:12px;color:var(--ink);cursor:pointer}
.tk svg{flex:none;color:var(--ink3);opacity:.5;transition:opacity .1s}
.tk:hover{border-color:var(--ink3)}.tk:hover svg{opacity:1;color:var(--ink)}
.tk--grp{background:none;border-color:transparent;padding-left:0;cursor:default;color:var(--ink2)}
.vc{cursor:pointer}.vc .sw{margin-right:10px}
.vt{display:inline-flex;flex-direction:column;vertical-align:middle;line-height:1.35;font-family:ui-monospace,Menlo,monospace}
.vt b{font-weight:500;font-size:12px;color:var(--ink)}.vt span{font-size:11px;color:var(--ink3)}
.vc:hover .vt b{text-decoration:underline}
.smpc{line-height:0}
.tw--card table.t td.smpc{overflow:visible}
.sbox{display:inline-flex;align-items:center;justify-content:center;min-width:52px;height:32px;border-radius:6px;background:var(--pv);border:1px solid var(--pv-line);box-sizing:border-box}
.sbox--dark{background:#2B2B2B;border-color:transparent;padding:0 6px}
.sbox--fill{border-color:rgba(0,0,0,.08)}
.sbox--pad{padding:0 4px}
.aa{font-size:17px;font-weight:600;line-height:1}
.bx{display:block;width:40px;height:22px;border:1.5px solid;border-radius:4px;box-sizing:border-box}
.fcs{display:block;width:40px;height:20px;border-radius:5px;background:#fff;border:1px solid #D2D2D2;box-sizing:border-box}
.shd{display:block;width:44px;height:22px;border-radius:5px;background:#fff}
"""


# ── 컬러 ──────────────────────────────────────────────────────────────
def color_page(d, stamp):
    prim = [r for r in d["layers"]["primitive"] if r["name"].startswith("color/")]
    sem = [r for r in d["layers"].get("semantic", []) if r["name"].startswith("color/")]
    hues = {}
    for r in prim:
        hues.setdefault(r["name"].split("/")[1], []).append(r)
    order = [h for h in HUE_ORDER if h in hues] + sorted(h for h in hues if h not in HUE_ORDER)
    rows = []
    for h in order:
        cells = []
        for r in sorted(hues[h], key=lambda x: step_key(x["name"])):
            step = r["name"].split("/")[-1]
            cells.append('<button type="button" class="pal__c" data-cp="var(%s)" title="%s · %s"><span class="pal__sw" style="background:%s"></span><span class="pal__s">%s</span><span class="pal__v">%s</span></button>'
                         % (esc(r["cssVar"]), esc(r["name"]), esc(r["value"]), esc(r["value"]), esc(step), esc(r["value"] if str(r["value"]).startswith("#") else alpha_label(r["value"]))))
        rows.append('<div class="pal"><div class="pal__h">%s<small>%d</small></div><div class="pal__r">%s</div></div>' % (esc(h), len(cells), "".join(cells)))
    groups = {}
    for r in sem:
        groups.setdefault(r["name"].split("/")[1], []).append(r)
    labels = dict(SEM_COLOR_GROUPS)
    gorder = [g for g, _ in SEM_COLOR_GROUPS if g in groups] + sorted(g for g in groups if g not in labels)
    tables = sem_color_tables(groups, labels, gorder)
    body = """
<h2>Color</h2>
<p class="sb-sub">primitive 팔레트 %d색 → semantic 역할 토큰 %d개. 화면에는 <b>역할 토큰</b>을 씁니다. 팔레트 값을 직접 쓰지 않습니다. 이름을 누르면 <code>var(--…)</code>가 복사됩니다.</p>
<div class="sec"><h3 class="sb-h3">Primitive — 팔레트<small>%d</small></h3><p class="lead">색상 계열별 단계입니다. 숫자가 클수록 진합니다. black·white는 투명도 단계(α)입니다.</p>%s</div>
<div class="sec"><h3 class="sb-h3">Semantic — 역할 토큰<small>%d</small></h3><p class="lead">바탕(bg) · 글자(fg) · 선(border) · 아이콘(icon) 등 역할로 고릅니다. 값이 바뀌어도 이름은 그대로라 화면이 따라옵니다.</p>
<label class="search"><input placeholder="brand, neutral, hover, #EB6100…" data-filter="table.t tr[data-k]" data-count=".count" autocomplete="off" aria-label="토큰 검색"><span class="count"></span><kbd>/</kbd></label>%s</div>
""" % (len(prim), len(sem), len(prim), "".join(rows), len(sem), tables)
    css = SEM_TABLE_CSS + r"""
.pal{margin:0 0 10px}.pal__h{font-size:12px;font-weight:700;color:var(--ink2);margin:0 0 4px;text-transform:uppercase;letter-spacing:.04em}.pal__h small{margin-left:6px;color:var(--ink3);font-weight:400;text-transform:none}
.pal__r{display:flex;flex-wrap:wrap;gap:4px}
.pal__c{display:flex;flex-direction:column;align-items:center;gap:3px;width:64px;padding:0;border:0;background:none;cursor:pointer}
.pal__sw{display:block;width:64px;height:40px;border-radius:7px;border:1px solid var(--pv-line);background-image:linear-gradient(45deg,#ddd 25%,transparent 25%),linear-gradient(-45deg,#ddd 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ddd 75%),linear-gradient(-45deg,transparent 75%,#ddd 75%);background-size:8px 8px;background-position:0 0,0 4px,4px -4px,-4px 0}
.pal__c:hover .pal__sw{outline:2px solid var(--accent);outline-offset:1px}
.pal__s{font-size:11px;font-weight:600;color:var(--ink2)}.pal__v{font-size:10px;color:var(--ink3);font-family:ui-monospace,Menlo,monospace}
"""
    return {"id": "c-Color", "group": "파운데이션", "nav": "Color <small>%d</small>" % (len(prim) + len(sem)), "body": body, "css": css}


# ── 넘버 ──────────────────────────────────────────────────────────────
def num_preview(group, v, name=""):
    px = "%spx" % v
    if group == "shadow":
        sh = "0 0 %s rgba(0,0,0,.25)" % px if "blur" in name else "0 %s 4px rgba(0,0,0,.25)" % px
        return '<span class="sbox sbox--pad"><i class="shd" style="box-shadow:%s"></i></span>' % sh
    if group == "size":
        return '<i class="nm nm--size" style="height:%s"></i>' % px
    if group == "spacing":
        return '<i class="nm nm--gap"><b></b><u style="width:%s"></u><b></b></i>' % px
    if group == "radius":
        return '<i class="nm nm--radius" style="border-radius:%s"></i>' % px
    if group == "border":
        return '<i class="nm nm--border" style="border-top-width:%s"></i>' % px
    if group == "icon":
        return '<i class="nm nm--icon" style="width:%s;height:%s"></i>' % (px, px)
    if group == "focus":
        return '<i class="nm nm--focus" style="box-shadow:0 0 0 %s var(--accent)"></i>' % px
    return ""


def number_page(d, stamp):
    prim = [r for r in d["layers"]["primitive"] if r["name"].startswith("number/")]
    sem = [r for r in d["layers"].get("semantic", []) if r["name"].startswith("number/")]
    rows = []
    vals = [r for r in prim if isinstance(num(r["value"]), (int, float))]
    top = max((float(num(r["value"])) for r in vals if float(num(r["value"])) < 999), default=1)
    for r in sorted(vals, key=lambda x: float(num(x["value"]))):
        f = num(r["value"]); full = f >= 999
        cls = "nsv__bar--full" if full else ("nsv__bar--base" if f and f % 4 == 0 else "")
        w = 100 if full else max(0.6, f / top * 100)
        rows.append('<button type="button" class="nsv__r" data-cp="var(%s)" title="%s"><code class="nsv__n">%s</code><i class="nsv__bar %s" style="width:%.1f%%"></i><span class="nsv__v">%s</span></button>'
                    % (esc(r["cssVar"]), esc(r["name"]), "full" if full else esc(f), cls, w, "full" if full else "%spx" % esc(f)))
    groups = {}
    for r in sem:
        groups.setdefault(r["name"].split("/")[1], []).append(r)
    labels = dict(SEM_NUMBER_GROUPS)
    gorder = [g for g, _ in SEM_NUMBER_GROUPS if g in groups] + sorted(g for g in groups if g not in labels)
    tables = sem_number_tables(groups, labels, gorder)
    body = """
<h2>Number</h2>
<p class="sb-sub">primitive 스케일 %d단계 → semantic 역할 토큰 %d개. 높이·간격·모서리·선 두께는 <b>역할 토큰</b>으로 씁니다. 이름을 누르면 <code>var(--…)</code>가 복사됩니다.</p>
<div class="sec"><h3 class="sb-h3">Primitive — 스케일<small>%d</small></h3><p class="lead">막대 길이가 값입니다. 4의 배수가 스케일의 근간이고(주황 막대), 그 사이 값은 타이포·대형 레이아웃용입니다(회색). full(999)은 원형에 씁니다(점선).</p>
<div class="nsv">%s</div></div>
<div class="sec"><h3 class="sb-h3">Semantic — 역할 토큰<small>%d</small></h3><p class="lead">컨트롤 높이(size) · 여백(spacing, 2px 배수) · 모서리(radius) · 선 두께(border) 등 역할로 고릅니다.</p>
<label class="search"><input placeholder="spacing, radius, 12, md…" data-filter="table.t tr[data-k]" data-count=".count" autocomplete="off" aria-label="토큰 검색"><span class="count"></span><kbd>/</kbd></label>%s</div>
""" % (len(prim), len(sem), len(prim), "".join(rows), len(sem), tables)
    css = r"""
.nsv{display:flex;flex-direction:column;gap:2px;max-width:760px}
.nsv__r{display:grid;grid-template-columns:56px minmax(0,1fr) 64px;align-items:center;gap:14px;border:0;background:none;padding:4px 6px;margin:0 -6px;border-radius:6px;cursor:pointer;text-align:left}
.nsv__r:hover{background:var(--chip)}
.nsv__n{font-size:12px;color:var(--ink2);text-align:right}
.nsv__bar{display:block;height:12px;border-radius:3px;background:var(--ink3);opacity:.5;min-width:2px}
.nsv__bar--base{background:var(--accent);opacity:1}
.nsv__bar--full{background:repeating-linear-gradient(90deg,var(--ink3) 0 6px,transparent 6px 10px);opacity:.7}
.nsv__v{font-size:12px;color:var(--ink3);font-family:ui-monospace,Menlo,monospace}
.nm{display:inline-block;vertical-align:middle}
.nm--size{width:24px;background:var(--accent);border-radius:3px}
.nm--gap{display:inline-flex;align-items:center}.nm--gap b{width:14px;height:14px;background:var(--ink3);border-radius:2px}.nm--gap u{display:inline-block;height:14px;background:var(--accent-soft);border-left:1px solid var(--accent);border-right:1px solid var(--accent)}
.nm--radius{width:32px;height:32px;border:2px solid var(--ink2)}
.nm--border{width:48px;border-top:0 solid var(--ink)}
.nm--icon{background:var(--ink3);border-radius:3px;opacity:.6}
.nm--focus{width:24px;height:24px;border-radius:6px;background:var(--card);border:1px solid var(--line)}
"""
    return {"id": "c-Number", "group": "파운데이션", "nav": "Number <small>%d</small>" % (len(prim) + len(sem)), "body": body, "css": css}


# ── 타이포그래피 ────────────────────────────────────────────────────────
def typography_page(d, stamp):
    ty = d["layers"]["typography"]
    fam = next((r["value"] for r in ty if r["name"] == "font-family/base"), "Pretendard")
    sizes = sorted([r for r in ty if r["name"].startswith("font-size/")], key=lambda r: float(num(r["value"])))
    lhs = sorted([r for r in ty if r["name"].startswith("line-height/")], key=lambda r: float(num(r["value"])))
    weights = sorted([r for r in ty if r["name"].startswith("font-weight/")], key=lambda r: int(num(r["css"])))
    wrow = "".join('<div class="w"><span style="font-weight:%s">가나다 ABC 123</span><code class="cp" data-cp="var(%s)">%s · %s</code></div>'
                   % (esc(r["css"]), esc(r["cssVar"]), esc(r["name"].split("/")[-1]), esc(r["css"])) for r in weights)
    srow = "".join('<div class="sz"><span style="font-size:%spx;line-height:1.3">가나다라 Aa 123</span><code class="cp" data-cp="var(%s)">%s</code></div>'
                   % (esc(num(r["value"])), esc(r["cssVar"]), esc(num(r["value"]))) for r in sizes)
    lrow = ", ".join('<code class="cp" data-cp="var(%s)">%s</code>' % (esc(r["cssVar"]), esc(num(r["value"]))) for r in lhs)
    styles = d["textStyles"]
    def skey(s):
        role, size, w = (s["name"].split("/") + ["", ""])[:3]
        return (0 if role == "title" else 1, -float(s["size"]), -int(s["weight"]) if str(s["weight"]).isdigit() else 0)
    groups = {}
    for s in sorted(styles, key=skey):
        groups.setdefault(s["name"].split("/")[0], []).append(s)
    tables = []
    for role, items in groups.items():
        trs = []
        for s in items:
            style = "font-weight:%s;font-size:%spx;line-height:%spx;font-family:%s" % (s["weight"], s["size"], s["lineHeight"], esc(fam))
            k = " ".join([s["name"], str(s["size"]), str(s["weight"]), s.get("description") or ""]).lower()
            trs.append('<tr data-k="%s"><td>%s</td><td><span class="smp" style="%s">환자 등록 · Patient 01</span></td><td><code>%s / %s</code></td><td><code>%s</code></td><td>%s</td></tr>'
                       % (esc(k), cp(s["name"]), style, esc(s["size"]), esc(s["lineHeight"]), esc(s["weight"]), cp(s["css"], "CSS 복사")))
        tables.append('<div class="sec" data-group><h4 class="sb-h4">%s<small>%d</small></h4><div class="tw tw--card"><table class="t ts"><colgroup><col style="width:220px"><col><col style="width:110px"><col style="width:80px"><col style="width:96px"></colgroup><thead><tr><th>스타일 (클릭 = 이름 복사)</th><th>표본</th><th>크기 / 행간</th><th>웨이트</th><th></th></tr></thead><tbody>%s</tbody></table></div></div>'
                      % (esc({"title": "title — 제목", "body": "body — 본문"}.get(role, role)), len(trs), "".join(trs)))
    body = """
<h2>Typography</h2>
<p class="sb-sub">글꼴 1종 · 웨이트 %d · 크기 %d단계 · 행간 %d단계 · 텍스트 스타일 %d개. 글은 <b>텍스트 스타일</b>로 고릅니다(<code>역할/크기/웨이트</code>). 같은 16px이라도 title/xs와 body/lg는 행간이 다릅니다.</p>
<div class="sec"><h3 class="sb-h3">글꼴<small>%s</small></h3><p class="lead">기본 글꼴은 <code class="cp" data-cp="var(--font-family-base)">%s</code>입니다. 설치돼 있지 않으면 시스템 산세리프로 대체됩니다.</p><div class="wrow">%s</div></div>
<div class="sec"><h3 class="sb-h3">크기 스케일<small>%d</small></h3><p class="lead">font-size 토큰입니다. 행간 토큰: %s</p><div class="srow">%s</div></div>
<div class="sec"><h3 class="sb-h3">텍스트 스타일<small>%d</small></h3><p class="lead">title은 제목 자리, body는 그 밖의 모든 글입니다. CSS 복사를 누르면 <code>font:</code> 한 줄이 복사됩니다.</p>
<label class="search"><input placeholder="title, body/md, 14, semibold…" data-filter="table.t tr[data-k]" data-count="#cnt" autocomplete="off" aria-label="스타일 검색"><span class="count" id="cnt"></span><kbd>/</kbd></label>%s</div>
""" % (len(weights), len(sizes), len(lhs), len(styles), esc(fam), esc(fam), wrow, len(sizes), lrow, srow, len(styles), "".join(tables))
    css = r"""
.tw{overflow-x:auto}
.wrow{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.w{border:1px solid var(--line);border-radius:10px;padding:14px;background:var(--card)}.w span{display:block;font-size:22px;margin:0 0 6px}
.srow{display:flex;flex-direction:column;gap:6px}
.sz{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding:6px 0}.sz span{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.smp{display:inline-block;white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis;vertical-align:middle}
table.ts{table-layout:fixed;min-width:640px}
table.ts td:nth-child(2){overflow:hidden}
"""
    return {"id": "c-Typography", "group": "파운데이션", "nav": "Typography <small>%d</small>" % len(styles), "body": body, "css": css}


# ── 홈 ────────────────────────────────────────────────────────────────
def index_page(d, stamp, nicons):
    pc = sum(1 for r in d["layers"]["primitive"] if r["name"].startswith("color/")); sc = sum(1 for r in d["layers"].get("semantic", []) if r["name"].startswith("color/"))
    pn = sum(1 for r in d["layers"]["primitive"] if r["name"].startswith("number/")); sn = sum(1 for r in d["layers"].get("semantic", []) if r["name"].startswith("number/"))
    cards = [("#c-Icon", "아이콘", "%d개 · 세트별 선/면 · 검색 · SVG 내려받기" % nicons),
             ("#c-Color", "컬러", "팔레트 %d · 역할 토큰 %d" % (pc, sc)),
             ("#c-Number", "넘버", "스케일 %d · 역할 토큰 %d (높이·간격·모서리·선)" % (pn, sn)),
             ("#c-Typography", "타이포그래피", "텍스트 스타일 %d · 크기 %d단계" % (len(d["textStyles"]), sum(1 for r in d["layers"]["typography"] if r["name"].startswith("font-size/"))))]
    body = """
<h2>시작하기</h2>
<p class="sb-sub">Cloud X 디자인시스템의 기초 자산 — 아이콘 · 컬러 · 넘버 · 타이포그래피. 다른 부서가 그대로 가져다 쓰는 공유본입니다. 기준: Figma %s.</p>
<div class="cards">%s</div>
<div class="sec"><h3 class="sb-h3">쓰는 법</h3><p class="lead">tokens.css 한 장을 넣고 변수로 씁니다. 아이콘은 sprite.svg를 두고 <code>&lt;use&gt;</code>로 참조합니다.</p>
<pre class="code"><code>&lt;link rel="stylesheet" href="tokens.css"&gt;

.card {
  background: var(--color-bg-surface-surface01);
  color: var(--color-fg-neutral-strong);
  padding: var(--number-spacing-x6);
  border-radius: var(--number-radius-lg);
  font: var(--font-weight-regular) var(--font-size-14) / var(--line-height-20) var(--font-family-base);
}

&lt;svg class="icon"&gt;&lt;use href="sprite.svg#i-00_general-search"/&gt;&lt;/svg&gt;
.icon { width: 20px; height: 20px; color: var(--color-fg-neutral-strong); }</code></pre></div>
<div class="sec"><h3 class="sb-h3">내려받기</h3><div class="dl">
<a class="btn btn--dark" href="tokens.css" download>tokens.css</a><a class="btn" href="cloudx-icons.zip" download>아이콘 ZIP</a></div>
<p class="lead" style="margin-top:10px">tokens.css는 primitive(팔레트·스케일) · semantic(역할) · typography 변수입니다. 아이콘 ZIP에는 낱개 SVG · sprite.svg · icons.json이 들어 있습니다. 기계용 토큰 목록(참조 체인·설명·텍스트 스타일 포함)이 필요하면 <a href="tokens.json" download>tokens.json</a>을 받습니다.</p></div>
""" % (esc(stamp), "".join('<a class="card" href="%s"><b>%s</b><span>%s</span></a>' % (h, t, s) for h, t, s in cards))
    css = r"""
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:0 0 32px}
.card{display:flex;flex-direction:column;gap:6px;padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--card);text-decoration:none}
.card b{font-size:17px}.card span{font-size:12.5px;color:var(--ink3)}
.card:hover{border-color:var(--accent)}
pre.code{margin:0;padding:14px;border:1px solid var(--line);border-radius:10px;background:var(--code-bg);font-size:12.5px;line-height:1.6;color:var(--ink2);overflow:auto}
.dl{display:flex;gap:8px;flex-wrap:wrap}
"""
    return {"id": "g-Intro", "group": "안내", "nav": "시작하기", "body": body, "css": css}


def sections(d, stamp, nicons):
    """절 목록 — 안내(시작하기) · Color · Number · Typography. Icon 절은 build-gallery.py 가 만든다."""
    return [index_page(d, stamp, nicons), color_page(d, stamp), number_page(d, stamp), typography_page(d, stamp)]


def main():
    d = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf-8"))
    print("절 %d개 — build-site.py 가 index.html 로 묶는다" % len(sections(d, d["source"].get("exportedAt") or "", 0)), file=sys.stderr)


if __name__ == "__main__":
    main()
