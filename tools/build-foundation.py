#!/usr/bin/env python3
"""tokens.json → index.html(홈) · color.html · number.html · typography.html

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


def swatch(value):
    return '<span class="sw"><i style="background:%s"></i></span>' % esc(value)


def cp(text, label=None):
    return '<code class="cp" data-cp="%s" title="클릭하면 복사">%s</code>' % (esc(text), esc(label if label is not None else text))


# ── 컬러 ──────────────────────────────────────────────────────────────
def color_page(d, stamp):
    prim = [r for r in d["layers"]["primitive"] if r["name"].startswith("color/")]
    sem = [r for r in d["layers"]["semantic"] if r["name"].startswith("color/")]
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
                         % (esc(r["cssVar"]), esc(r["name"]), esc(r["value"]), esc(r["value"]), esc(step), esc(r["value"] if str(r["value"]).startswith("#") else "α")))
        rows.append('<div class="pal"><div class="pal__h">%s<small>%d</small></div><div class="pal__r">%s</div></div>' % (esc(h), len(cells), "".join(cells)))
    groups = {}
    for r in sem:
        groups.setdefault(r["name"].split("/")[1], []).append(r)
    gorder = [g for g, _ in SEM_COLOR_GROUPS if g in groups] + sorted(g for g in groups if g not in dict(SEM_COLOR_GROUPS))
    labels = dict(SEM_COLOR_GROUPS)
    tables = []
    for g in gorder:
        trs = []
        for r in sorted(groups[g], key=lambda x: x["name"]):
            short = r["name"][len("color/"):]
            k = " ".join([r["name"], str(r["value"]), r.get("alias") or "", r.get("description") or ""]).lower()
            trs.append('<tr data-k="%s"><td>%s</td><td>%s</td><td><code class="cp" data-cp="%s">%s</code></td><td class="mut">%s</td><td class="mut">%s</td></tr>'
                       % (esc(k), cp("var(%s)" % r["cssVar"], short), swatch(r["value"]), esc(r["value"]), esc(r["value"]),
                          esc((r.get("alias") or "").replace("color/", "")), esc(r.get("description") or "")))
        tables.append('<div class="sec" data-group><h2>%s<small class="n">%d</small></h2><div class="tw"><table class="t"><thead><tr><th>이름 (클릭 = CSS 변수 복사)</th><th></th><th>값</th><th>참조(primitive)</th><th>설명</th></tr></thead><tbody>%s</tbody></table></div></div>'
                      % (esc(labels.get(g, g)), len(trs), "".join(trs)))
    body = """
<h1 class="pg-h">컬러</h1>
<p class="pg-sub">primitive 팔레트 %d색 → semantic 역할 토큰 %d개. 화면에는 <b>semantic 토큰</b>을 씁니다. 팔레트 값을 직접 쓰지 않습니다. 이름을 누르면 <code>var(--…)</code>가 복사됩니다.</p>
<div class="sec"><h2>Primitive — 팔레트<small class="n">%d</small></h2><p class="lead">색상 계열별 단계입니다. 숫자가 클수록 진합니다. black·white는 투명도 단계(α)입니다. 칸을 누르면 변수 이름이 복사됩니다.</p>%s</div>
<div class="sec"><h2>Semantic — 역할 토큰<small class="n">%d</small></h2><p class="lead">바탕(bg) · 글자(fg) · 선(border) · 아이콘(icon) 등 역할로 고릅니다. 값이 바뀌어도 이름은 그대로라 화면이 따라옵니다.</p>
<label class="search"><input placeholder="brand, neutral, hover, #EB6100…" data-filter="table.t tr[data-k]" data-count="#cnt" autocomplete="off" aria-label="토큰 검색"><span class="count" id="cnt"></span><kbd>/</kbd></label>%s</div>
""" % (len(prim), len(sem), len(prim), "".join(rows), len(sem), "".join(tables))
    css = r"""
.n{margin-left:8px;color:var(--ink3);font-weight:400;font-size:12px}
.tw{overflow-x:auto}
.pal{margin:0 0 10px}.pal__h{font-size:12px;font-weight:700;color:var(--ink2);margin:0 0 4px;text-transform:uppercase;letter-spacing:.04em}.pal__h small{margin-left:6px;color:var(--ink3);font-weight:400;text-transform:none}
.pal__r{display:flex;flex-wrap:wrap;gap:4px}
.pal__c{display:flex;flex-direction:column;align-items:center;gap:3px;width:64px;padding:0;border:0;background:none;cursor:pointer}
.pal__sw{display:block;width:64px;height:40px;border-radius:7px;border:1px solid var(--pv-line);background-image:linear-gradient(45deg,#ddd 25%,transparent 25%),linear-gradient(-45deg,#ddd 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ddd 75%),linear-gradient(-45deg,transparent 75%,#ddd 75%);background-size:8px 8px;background-position:0 0,0 4px,4px -4px,-4px 0}
.pal__c:hover .pal__sw{outline:2px solid var(--accent);outline-offset:1px}
.pal__s{font-size:11px;font-weight:600;color:var(--ink2)}.pal__v{font-size:10px;color:var(--ink3);font-family:ui-monospace,Menlo,monospace}
.mut{color:var(--ink3);font-size:12px}
"""
    return page.render("Cloud X Foundation · 컬러", "color.html", body, css=css, desc="Cloud X 컬러 토큰 — 팔레트와 역할 토큰", stamp=stamp)


# ── 넘버 ──────────────────────────────────────────────────────────────
def num_preview(group, v):
    px = "%spx" % v
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
    sem = [r for r in d["layers"]["semantic"] if r["name"].startswith("number/")]
    bars = []
    for r in sorted(prim, key=lambda x: float(num(x["value"]) if isinstance(num(x["value"]), (int, float)) else 0)):
        f = num(r["value"]); full = isinstance(f, (int, float)) and f >= 999
        cls = "ns__bar--full" if full else ("ns__bar--base" if isinstance(f, (int, float)) and f and f % 4 == 0 else "")
        bars.append('<button type="button" class="ns__col" data-cp="var(%s)" title="%s · %spx"><i class="%s" style="height:%dpx"></i><span>%s</span></button>'
                    % (esc(r["cssVar"]), esc(r["name"]), esc(f), cls, 96 if full else max(1, round(float(f) * 0.5)) if isinstance(f, (int, float)) else 1, "full" if full else esc(f)))
    groups = {}
    for r in sem:
        groups.setdefault(r["name"].split("/")[1], []).append(r)
    labels = dict(SEM_NUMBER_GROUPS)
    gorder = [g for g, _ in SEM_NUMBER_GROUPS if g in groups] + sorted(g for g in groups if g not in labels)
    tables = []
    for g in gorder:
        trs = []
        for r in sorted(groups[g], key=lambda x: (float(num(x["value"])) if isinstance(num(x["value"]), (int, float)) else 0, x["name"])):
            short = r["name"][len("number/"):]
            k = " ".join([r["name"], str(r["value"]), r.get("alias") or "", r.get("description") or ""]).lower()
            trs.append('<tr data-k="%s"><td>%s</td><td>%s</td><td><code>%spx</code></td><td class="mut">%s</td><td class="mut">%s</td></tr>'
                       % (esc(k), cp("var(%s)" % r["cssVar"], short), num_preview(g, num(r["value"])), esc(num(r["value"])),
                          esc((r.get("alias") or "").replace("number/", "")), esc(r.get("description") or "")))
        tables.append('<div class="sec" data-group><h2>%s<small class="n">%d</small></h2><div class="tw"><table class="t"><thead><tr><th>이름 (클릭 = CSS 변수 복사)</th><th>미리보기</th><th>값</th><th>참조(primitive)</th><th>설명</th></tr></thead><tbody>%s</tbody></table></div></div>'
                      % (esc(labels.get(g, g)), len(trs), "".join(trs)))
    body = """
<h1 class="pg-h">넘버</h1>
<p class="pg-sub">primitive 스케일 %d단계 → semantic 역할 토큰 %d개. 높이·간격·모서리·선 두께는 <b>semantic 토큰</b>으로 씁니다. 이름을 누르면 <code>var(--…)</code>가 복사됩니다.</p>
<div class="sec"><h2>Primitive — 스케일<small class="n">%d</small></h2><p class="lead">막대 높이가 값입니다. 4의 배수가 스케일의 근간이고(진한 막대), 그 사이 값은 타이포·대형 레이아웃용입니다. full(999)은 원형에 씁니다.</p>
<div class="ns">%s</div></div>
<div class="sec"><h2>Semantic — 역할 토큰<small class="n">%d</small></h2><p class="lead">컨트롤 높이(size) · 여백(spacing, 2px 배수) · 모서리(radius) · 선 두께(border) 등 역할로 고릅니다.</p>
<label class="search"><input placeholder="spacing, radius, 12, md…" data-filter="table.t tr[data-k]" data-count="#cnt" autocomplete="off" aria-label="토큰 검색"><span class="count" id="cnt"></span><kbd>/</kbd></label>%s</div>
""" % (len(prim), len(sem), len(prim), "".join(bars), len(sem), "".join(tables))
    css = r"""
.n{margin-left:8px;color:var(--ink3);font-weight:400;font-size:12px}
.tw{overflow-x:auto}
.ns{display:flex;align-items:flex-end;gap:6px;flex-wrap:wrap;padding:12px 0 4px}
.ns__col{display:flex;flex-direction:column;align-items:center;gap:4px;width:34px;border:0;background:none;padding:0;cursor:pointer}
.ns__col i{display:block;width:22px;border-radius:3px 3px 0 0;background:var(--ink3);opacity:.55}
.ns__col i.ns__bar--base{background:var(--accent);opacity:1}
.ns__col i.ns__bar--full{background:repeating-linear-gradient(180deg,var(--ink3) 0 4px,transparent 4px 8px);opacity:.7}
.ns__col span{font-size:10px;color:var(--ink3);font-family:ui-monospace,Menlo,monospace}
.ns__col:hover i{outline:2px solid var(--accent);outline-offset:1px}
.nm{display:inline-block;vertical-align:middle}
.nm--size{width:24px;background:var(--accent);border-radius:3px}
.nm--gap{display:inline-flex;align-items:center}.nm--gap b{width:14px;height:14px;background:var(--ink3);border-radius:2px}.nm--gap u{display:inline-block;height:14px;background:var(--accent-soft);border-left:1px solid var(--accent);border-right:1px solid var(--accent)}
.nm--radius{width:32px;height:32px;border:2px solid var(--ink2)}
.nm--border{width:48px;border-top:0 solid var(--ink)}
.nm--icon{background:var(--ink3);border-radius:3px;opacity:.6}
.nm--focus{width:24px;height:24px;border-radius:6px;background:var(--card);border:1px solid var(--line)}
.mut{color:var(--ink3);font-size:12px}
"""
    return page.render("Cloud X Foundation · 넘버", "number.html", body, css=css, desc="Cloud X 수치 토큰 — 스케일과 역할 토큰", stamp=stamp)


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
        tables.append('<div class="sec" data-group><h2>%s<small class="n">%d</small></h2><div class="tw"><table class="t"><thead><tr><th>스타일 (클릭 = 이름 복사)</th><th>표본</th><th>크기 / 행간</th><th>웨이트</th><th></th></tr></thead><tbody>%s</tbody></table></div></div>'
                      % (esc({"title": "title — 제목", "body": "body — 본문"}.get(role, role)), len(trs), "".join(trs)))
    body = """
<h1 class="pg-h">타이포그래피</h1>
<p class="pg-sub">글꼴 1종 · 웨이트 %d · 크기 %d단계 · 행간 %d단계 · 텍스트 스타일 %d개. 글은 <b>텍스트 스타일</b>로 고릅니다(<code>역할/크기/웨이트</code>). 같은 16px이라도 title/xs와 body/lg는 행간이 다릅니다.</p>
<div class="sec"><h2>글꼴<small class="n">%s</small></h2><p class="lead">기본 글꼴은 <code class="cp" data-cp="var(--font-family-base)">%s</code>입니다. 설치돼 있지 않으면 시스템 산세리프로 대체됩니다.</p><div class="wrow">%s</div></div>
<div class="sec"><h2>크기 스케일<small class="n">%d</small></h2><p class="lead">font-size 토큰입니다. 행간 토큰: %s</p><div class="srow">%s</div></div>
<div class="sec"><h2>텍스트 스타일<small class="n">%d</small></h2><p class="lead">title은 제목 자리, body는 그 밖의 모든 글입니다. CSS 복사를 누르면 <code>font:</code> 한 줄이 복사됩니다.</p>
<label class="search"><input placeholder="title, body/md, 14, semibold…" data-filter="table.t tr[data-k]" data-count="#cnt" autocomplete="off" aria-label="스타일 검색"><span class="count" id="cnt"></span><kbd>/</kbd></label>%s</div>
""" % (len(weights), len(sizes), len(lhs), len(styles), esc(fam), esc(fam), wrow, len(sizes), lrow, srow, len(styles), "".join(tables))
    css = r"""
.n{margin-left:8px;color:var(--ink3);font-weight:400;font-size:12px}
.tw{overflow-x:auto}
.wrow{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.w{border:1px solid var(--line);border-radius:10px;padding:14px;background:var(--card)}.w span{display:block;font-size:22px;margin:0 0 6px}
.srow{display:flex;flex-direction:column;gap:6px}
.sz{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding:6px 0}.sz span{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.smp{display:inline-block;white-space:nowrap}
"""
    return page.render("Cloud X Foundation · 타이포그래피", "typography.html", body, css=css, desc="Cloud X 타이포그래피 — 글꼴·크기·텍스트 스타일", stamp=stamp)


# ── 홈 ────────────────────────────────────────────────────────────────
def index_page(d, stamp, nicons):
    pc = sum(1 for r in d["layers"]["primitive"] if r["name"].startswith("color/")); sc = sum(1 for r in d["layers"]["semantic"] if r["name"].startswith("color/"))
    pn = sum(1 for r in d["layers"]["primitive"] if r["name"].startswith("number/")); sn = sum(1 for r in d["layers"]["semantic"] if r["name"].startswith("number/"))
    cards = [("icons.html", "아이콘", "%d개 · 세트별 선/면 · 검색 · SVG 내려받기" % nicons),
             ("color.html", "컬러", "팔레트 %d · 역할 토큰 %d" % (pc, sc)),
             ("number.html", "넘버", "스케일 %d · 역할 토큰 %d (높이·간격·모서리·선)" % (pn, sn)),
             ("typography.html", "타이포그래피", "텍스트 스타일 %d · 크기 %d단계" % (len(d["textStyles"]), sum(1 for r in d["layers"]["typography"] if r["name"].startswith("font-size/"))))]
    body = """
<h1 class="pg-h">Cloud X Foundation</h1>
<p class="pg-sub">Cloud X 디자인시스템의 기초 자산 — 아이콘 · 컬러 · 넘버 · 타이포그래피. 다른 부서가 그대로 가져다 쓰는 공유본입니다. 기준: Figma %s.</p>
<div class="cards">%s</div>
<div class="sec"><h2>시작하기</h2><p class="lead">tokens.css 한 장을 넣고 변수로 씁니다. 아이콘은 sprite.svg를 두고 <code>&lt;use&gt;</code>로 참조합니다.</p>
<pre class="code"><code>&lt;link rel="stylesheet" href="tokens.css"&gt;

.card {
  background: var(--color-bg-surface-surface01);
  color: var(--color-fg-neutral-strong);
  padding: var(--number-spacing-x6);
  border-radius: var(--number-radius-lg);
  font: var(--font-weight-regular) var(--font-size-14) / var(--line-height-20) var(--font-family-base);
}

&lt;svg class="icon"&gt;&lt;use href="sprite.svg#i-00_general-search"/&gt;&lt;/svg&gt;
.icon { width: 20px; height: 20px; color: var(--color-icon-neutral-strong); }</code></pre></div>
<div class="sec"><h2>내려받기</h2><div class="dl">
<a class="btn btn--dark" href="tokens.css" download>tokens.css</a><a class="btn" href="tokens.json" download>tokens.json</a><a class="btn" href="cloudx-icons.zip" download>아이콘 ZIP</a><a class="btn" href="sprite.svg" download>sprite.svg</a></div>
<p class="lead" style="margin-top:10px">tokens.css는 primitive · semantic · typography 변수, tokens.json은 같은 토큰에 참조 체인·설명·텍스트 스타일을 더한 기계용 목록입니다.</p></div>
""" % (esc(stamp), "".join('<a class="card" href="%s"><b>%s</b><span>%s</span></a>' % (h, t, s) for h, t, s in cards))
    css = r"""
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:0 0 32px}
.card{display:flex;flex-direction:column;gap:6px;padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--card);text-decoration:none}
.card b{font-size:17px}.card span{font-size:12.5px;color:var(--ink3)}
.card:hover{border-color:var(--accent)}
pre.code{margin:0;padding:14px;border:1px solid var(--line);border-radius:10px;background:var(--code-bg);font-size:12.5px;line-height:1.6;color:var(--ink2);overflow:auto}
.dl{display:flex;gap:8px;flex-wrap:wrap}
"""
    js = "if (/^#icon=/.test(location.hash)) location.replace('icons.html' + location.hash);"
    return page.render("Cloud X Foundation", "index.html", body, css=css, js=js, desc="Cloud X 디자인시스템 기초 자산 — 아이콘·컬러·넘버·타이포그래피", stamp=stamp)


def main():
    d = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf-8"))
    stamp = d["source"].get("exportedAt") or ""
    ip = os.path.join(ROOT, "icons.json")
    nicons = json.load(open(ip, encoding="utf-8"))["count"] if os.path.exists(ip) else 0
    for fn, fnc in (("color.html", color_page), ("number.html", number_page), ("typography.html", typography_page)):
        open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(fnc(d, stamp))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index_page(d, stamp, nicons))
    print("index.html · color.html · number.html · typography.html — Figma %s 기준" % stamp, file=sys.stderr)


if __name__ == "__main__":
    main()
