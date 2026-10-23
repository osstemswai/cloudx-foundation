#!/usr/bin/env python3
"""meta/ + sprite.svg → Icon 절(section, build-site.py 가 index.html 에 넣음) · icons.json (기계용 목록) · cloudx-icons.zip

    python3 tools/build-gallery.py

스프라이트는 절 꼬리(tail)로 인라인됩니다. 뼈대(LNB·절 전환)는 tools/page.py 입니다.
세트 순서는 Figma 캔버스 배치 순서(`meta/_sets.json`), 그림 크기는 `meta/_ink.json`,
한국어 검색어는 `meta/_keywords.json`에서 옵니다. 셋 다 cloudXDS에서 복사해 온 것이고
`tools/sync.py`가 갱신합니다.
"""
import os, re, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
META = os.path.join(ROOT, "meta")
REPO_URL = "https://github.com/osstemswai/cloudx-foundation"


def read(p):
    with open(p, encoding="utf-8") as fp:
        return fp.read()


def load_json(name, default):
    p = os.path.join(META, name)
    return json.loads(read(p)) if os.path.exists(p) else default


def keywords(cat, setname, files, kw):
    """검색어 — 카테고리·세트·파일명의 영문 토큰 + `_keywords.json`의 한국어 유의어."""
    toks = []
    for src in [re.sub(r"^\d+_", "", cat), setname] + list(files):
        for t in re.split(r"[/_\-\s]+", src.lower()):
            if t and not t.isdigit() and t not in toks:
                toks.append(t)
    ko = []
    for t in toks:
        for k in kw.get(t, []):
            if k not in ko and k not in toks:
                ko.append(k)
    return toks + ko


def vkey(v):
    """변형 순서를 선(Fill=off) → 면(Fill=on)으로. 파일명 규칙과 같습니다."""
    m = re.search(r"(?i)\bfill=(on|off)\b", v.get("variant") or "")
    if m and m.group(1).lower() == "off":
        return (0, "")
    return (1, "") if m else (2, v.get("variant") or "")


def collect():
    sets = load_json("_sets.json", {})
    ink = load_json("_ink.json", {})
    kw = {k: v for k, v in load_json("_keywords.json", {}).items() if not k.startswith("_")}
    cats = []
    for cat in sorted(sets):
        icons = []
        for item in sets[cat]:
            for v in sorted(item["variants"], key=vkey):
                fm = re.search(r"(?i)\bfill=(on|off)\b", v.get("variant") or "")
                wh = ink.get("%s/%s" % (cat, v["file"]))
                icons.append({
                    "id": "i-%s-%s" % (cat, v["file"]),
                    "category": cat,
                    "set": item["set"],
                    "name": v["file"],
                    "variant": v.get("variant") or "",
                    "fill": fm.group(1).lower() if fm else "",
                    "file": "svg/%s/%s.svg" % (cat, v["file"]),
                    "ink": wh or None,
                    "size": round(max(wh)) if wh else 0,
                    "keywords": keywords(cat, item["set"], [v["file"]], kw),
                })
        cats.append({"category": cat, "sets": len(sets[cat]), "icons": icons})
    return cats


# ── 페이지 ──────────────────────────────────────────────────────────────

CSS = r"""
.icl-wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:28px;align-items:start}
.tools{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:12px 0 4px}
.seg{display:inline-flex;background:var(--chip);border-radius:999px;padding:3px}
.seg button{border:0;background:none;font-size:12.5px;font-weight:600;color:var(--ink3);padding:6px 14px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--card);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.cats{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 22px}
.cats button{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:5px 11px;font-size:12px;color:var(--ink2);cursor:pointer}
.cats button small{color:var(--ink3);margin-left:4px}
.cats button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.cats button[aria-pressed="true"] small{color:inherit;opacity:.7}
.cat{margin:0 0 26px}
.cat[hidden]{display:none}
.cat h2{font-size:12px;margin:0 0 10px;color:var(--ink3);font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.cat h2 small{color:var(--ink3);opacity:.7;font-weight:400;text-transform:none;letter-spacing:0;margin-left:8px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:8px}
.c{display:flex;flex-direction:column;align-items:center;gap:7px;padding:14px 6px 9px;border:1px solid var(--pv-line);border-radius:10px;
   background:var(--pv);color:#1d1d1d;cursor:pointer;min-width:0;text-align:center}
.c svg{width:24px;height:24px;display:block}
.c span{font-size:11px;line-height:1.3;color:#6b6b6b;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.c:hover{border-color:#c4c4c6}
.c.on{background:#fef1e9;border-color:#f5af7d}
.c:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.c[hidden]{display:none}
.empty{display:none;padding:48px 0;text-align:center;color:var(--ink3)}
.empty.show{display:block}
.d{position:sticky;top:24px;border:1px solid var(--line);border-radius:14px;background:var(--card);padding:20px;max-height:calc(100vh - 48px);overflow:auto}
.d__empty{font-size:13px;color:var(--ink3);line-height:1.7}
.d__empty b{color:var(--ink2)}
.d__body[hidden]{display:none}
.d__name{margin:0 0 4px;font-size:16px;font-weight:700;word-break:break-all}
.d__sub{margin:0 0 10px;font-size:12px;color:var(--ink3)}
.d__kw{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 16px}
.d__kw span{font-size:11.5px;padding:3px 8px;border-radius:6px;background:var(--chip);color:var(--ink2)}
.pv{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 16px}
.pv div{height:84px;border-radius:10px;display:flex;align-items:center;justify-content:center;gap:16px;position:relative}
.pv .l{background:#f4f4f4;color:#1d1d1d;border:1px solid var(--pv-line)}
.pv .k{background:#1d1d1d;color:#ebebeb;border:1px solid var(--line)}
.pv div::after{content:attr(data-l);position:absolute;left:8px;bottom:5px;font-size:10px;opacity:.55}
.pv svg{display:block}
.tabs{display:flex;border-bottom:1px solid var(--line);margin:0 0 12px}
.tabs button{flex:1;border:0;background:none;font-size:13px;font-weight:600;color:var(--ink3);padding:8px 0;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px}
.tabs button.on{color:var(--ink);border-bottom-color:var(--ink)}
.pane[hidden]{display:none}
.lab{display:flex;align-items:center;justify-content:space-between;margin:4px 0 8px;font-size:12px;color:var(--ink2)}
.acts{display:inline-flex;gap:6px}
.sm{border:1px solid var(--line);background:var(--card);border-radius:6px;font-size:11.5px;color:var(--ink2);padding:3px 8px;cursor:pointer;text-decoration:none}
.sm:hover{background:var(--chip)}
pre.code{margin:0 0 12px;padding:12px;border:1px solid var(--line);border-radius:8px;background:var(--code-bg);font-size:11.5px;line-height:1.6;color:var(--ink2);overflow:auto;white-space:pre;max-height:200px}
pre.code--svg{max-height:240px}
.hint{margin:0 0 12px;font-size:11.5px;color:var(--ink3);line-height:1.7}
.hint code{font-size:11px;background:var(--chip);padding:1px 5px;border-radius:4px}
.fig{margin:0 0 6px;font-size:12.5px}
.fig b{font-weight:600}
.d__head{display:flex;align-items:flex-start;gap:10px}
.d__head .d__name{flex:1;min-width:0}
.d__close{display:none;flex:none;width:30px;height:30px;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;background:var(--card);cursor:pointer;padding:0}
.d__close svg{width:14px;height:14px}
@media (max-width:980px){
  .icl-wrap{grid-template-columns:1fr}
  .d{position:fixed;left:0;right:0;bottom:0;z-index:40;max-height:72vh;border-radius:16px 16px 0 0;box-shadow:0 -8px 30px rgba(0,0,0,.18);
     transform:translateY(105%);transition:transform .22s ease}
  .d.open{transform:none}
  .d__empty{display:none}
  .d__close{display:inline-flex}
}
"""

JS = r"""
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var d = $('#d'), body = $('.d__body', d), empty = $('.d__empty', d);
  var q = $('#q'), cells = $$('.c'), seg = $$('.seg button'), catBtns = $$('.cats button'), countEl = $('.count'), emptyMsg = $('.empty');
  var fill = '', cat = '', cur = null;

  function svgOf(id) {
    var sym = document.getElementById(id); if (!sym) return '';
    return '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">\n' + sym.innerHTML.trim() + '\n</svg>';
  }
  function select(el, remember) {
    if (cur) cur.classList.remove('on');
    cur = el; el.classList.add('on');
    var a = el.dataset, id = 'i-' + a.cat + '-' + a.file;
    body.hidden = false; empty.hidden = true;
    $('.d__name', d).textContent = a.file;
    $('.d__sub', d).textContent = a.cat + ' · ' + a.set + (a.variant ? ' · ' + a.variant : '') + (a.sz && a.sz !== '0' ? ' · 그림 ' + a.sz + 'px' : '');
    $('.d__kw', d).innerHTML = (a.k || '').split('|').filter(Boolean).map(function (k) { return '<span>' + esc(k) + '</span>'; }).join('');
    $$('.pv use', d).forEach(function (u) { u.setAttribute('href', '#' + id); });
    var sprite = '<svg class="icon" width="20" height="20" aria-hidden="true">\n  <use href="sprite.svg#' + id + '"/>\n</svg>';
    var inline = svgOf(id);
    var img = '<img src="svg/' + a.cat + '/' + a.file + '.svg" width="20" height="20" alt="">';
    $('[data-pane="sprite"] code', d).textContent = sprite;
    $('[data-pane="inline"] code', d).textContent = inline;
    $('[data-pane="img"] code', d).textContent = img;
    $('.fig b', d).textContent = a.set + (a.variant ? '  ›  ' + a.variant : '');
    d.dataset.sprite = sprite; d.dataset.inline = inline; d.dataset.img = img;
    var dl = $('.dl', d); dl.href = 'svg/' + a.cat + '/' + a.file + '.svg'; dl.download = a.file + '.svg';
    d.classList.add('open');
    if (remember) history.replaceState(null, '', '#c-Icon?icon=' + a.cat + '/' + encodeURIComponent(a.file));
  }
  function close() {
    d.classList.remove('open');
    if (cur) { cur.classList.remove('on'); cur = null; }
    history.replaceState(null, '', '#c-Icon');
  }
  function toast(msg) { if (window.cxToast) cxToast(msg); }
  document.addEventListener('click', function (e) {
    var c = e.target.closest('.c'); if (c) { select(c, true); return; }
    if (e.target.closest('.d__close')) { close(); return; }
    var tb = e.target.closest('.tabs button');
    if (tb) { $$('.tabs button', d).forEach(function (b) { b.classList.toggle('on', b === tb); });
              $$('.pane', d).forEach(function (p) { p.hidden = p.dataset.pane !== tb.dataset.tab; }); return; }
    var cp = e.target.closest('[data-copy]');
    if (cp) { var txt = d.dataset[cp.dataset.copy] || '';
              navigator.clipboard.writeText(txt).then(function () { toast('복사했습니다'); }, function () { toast('복사에 실패했습니다'); }); return; }
    var sb = e.target.closest('.seg button');
    if (sb) { fill = sb.dataset.fill; seg.forEach(function (b) { b.setAttribute('aria-pressed', String(b === sb)); }); filter(); return; }
    var cb = e.target.closest('.cats button');
    if (cb) { cat = cb.dataset.cat; catBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b === cb)); }); filter(); }
  });
  function filter() {
    var v = (q.value || '').trim().toLowerCase(), n = 0;
    cells.forEach(function (c) {
      var a = c.dataset;
      var ok = (!v || a.set.toLowerCase().indexOf(v) >= 0 || a.file.toLowerCase().indexOf(v) >= 0 || (a.k || '').indexOf(v) >= 0)
        && (!fill || a.fill === fill) && (!cat || a.cat === cat);
      c.hidden = !ok; if (ok) n++;
    });
    $$('.cat').forEach(function (g) { g.hidden = !g.querySelector('.c:not([hidden])'); });
    countEl.textContent = n + ' / ' + cells.length;
    emptyMsg.classList.toggle('show', n === 0);
  }
  q.addEventListener('input', filter);
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
    if (e.key === 'Escape') { if (document.activeElement === q) { q.value = ''; filter(); q.blur(); } else if (d.classList.contains('open')) close(); }
  });
  filter();

  /* 딥링크 — #c-Icon?icon=<카테고리>/<파일> (셸이 절을 보인 뒤 부른다) */
  window.icSelectFromHash = function () {
    var m = /[?&#]icon=([^&/]+)\/([^&]+)/.exec(location.hash); if (!m) return;
    var file = decodeURIComponent(m[2]);
    var hit = cells.filter(function (x) { return x.dataset.cat === m[1] && x.dataset.file === file; })[0];
    if (hit) { select(hit, false); hit.scrollIntoView({ block: 'center' }); }
  };
})();
"""

BODY = r"""
<h2>Icon</h2>
<p class="sb-sub">아이콘 {{N}} · 세트 {{NSET}} · 카테고리 {{NCAT}} — viewBox 0 0 20 20, 선(Fill=off)이 기본이고 면은 <code>-fill</code>. 색은 <code>color</code>로 줍니다.</p>
<div class="icl-wrap">
  <section>
    <label class="search"><svg viewBox="0 0 20 20" aria-hidden="true" style="width:18px;height:18px;color:var(--ink3);flex:none"><use href="#i-00_general-search"/></svg>
      <input id="q" placeholder="화살표, calendar, 검색, 환자…" autocomplete="off" aria-label="아이콘 검색"><kbd>/</kbd></label>
    <div class="tools">
      <div class="seg" role="group" aria-label="변형">
        <button type="button" data-fill="" aria-pressed="true">전체</button>
        <button type="button" data-fill="off" aria-pressed="false">선 · Fill=off</button>
        <button type="button" data-fill="on" aria-pressed="false">면 · Fill=on</button>
      </div>
      <span class="count"></span>
    </div>
    <div class="cats" role="group" aria-label="카테고리">
      <button type="button" data-cat="" aria-pressed="true">전체<small>{{N}}</small></button>
      {{CATBTNS}}
    </div>
    {{CATS}}
    <p class="empty">검색 결과가 없습니다. 영문 이름이나 한국어 뜻으로 다시 찾아보세요.</p>
  </section>

  <aside class="d" id="d" aria-live="polite">
    <div class="d__empty">아이콘을 누르면 여기에 이름 · 검색어 · 미리보기 · 코드가 나옵니다.<br><br>
      전부 필요하면 위의 <b>아이콘 ZIP</b>으로 낱개 SVG · sprite.svg · icons.json을 한 번에 받습니다.<br><br>
      <b>크기</b>는 16 · 20 · 24 중 하나로 주고, <b>색</b>은 <code>color</code>로 줍니다.<br>
      선(<code>Fill=off</code>)이 기본이고 면은 이름 뒤에 <code>-fill</code>이 붙습니다.</div>
    <div class="d__body" hidden>
      <div class="d__head"><div class="d__name mono"></div><button type="button" class="d__close" aria-label="닫기"><svg viewBox="0 0 20 20" aria-hidden="true"><use href="#i-00_window-Window-close"/></svg></button></div>
      <p class="d__sub"></p>
      <div class="d__kw"></div>
      <div class="pv">
        <div class="l" data-l="밝은 면 · 16 / 20 / 24">
          <svg width="16" height="16" viewBox="0 0 20 20"><use href="#"/></svg>
          <svg width="20" height="20" viewBox="0 0 20 20"><use href="#"/></svg>
          <svg width="24" height="24" viewBox="0 0 20 20"><use href="#"/></svg></div>
        <div class="k" data-l="어두운 면">
          <svg width="16" height="16" viewBox="0 0 20 20"><use href="#"/></svg>
          <svg width="20" height="20" viewBox="0 0 20 20"><use href="#"/></svg>
          <svg width="24" height="24" viewBox="0 0 20 20"><use href="#"/></svg></div>
      </div>
      <div class="tabs">
        <button type="button" class="on" data-tab="sprite">스프라이트</button>
        <button type="button" data-tab="inline">인라인 SVG</button>
        <button type="button" data-tab="img">img</button>
      </div>
      <div class="pane" data-pane="sprite">
        <div class="lab">HTML <span class="acts"><button type="button" class="sm" data-copy="sprite">복사</button></span></div>
        <pre class="code"><code></code></pre>
        <p class="hint"><code>sprite.svg</code> 한 파일을 프로젝트에 두고 <code>&lt;use&gt;</code>로 참조합니다. 색은 <code>color</code>를 따릅니다(<code>currentColor</code>).<br>
        <code>.icon { width:20px; height:20px; color:#1d1d1d }</code></p>
      </div>
      <div class="pane" data-pane="inline" hidden>
        <div class="lab">SVG <span class="acts"><button type="button" class="sm" data-copy="inline">복사</button><a class="sm dl" href="#" download>내려받기</a></span></div>
        <pre class="code code--svg"><code></code></pre>
        <p class="hint">HTML에 직접 넣거나 React 컴포넌트로 감쌉니다. 역시 <code>color</code>로 색을 줍니다.</p>
      </div>
      <div class="pane" data-pane="img" hidden>
        <div class="lab">HTML <span class="acts"><button type="button" class="sm" data-copy="img">복사</button></span></div>
        <pre class="code"><code></code></pre>
        <p class="hint"><code>svg/</code> 폴더를 통째로 두고 이미지처럼 씁니다. 가장 간단하지만 <b>색을 바꿀 수 없습니다</b>(검정 고정).</p>
      </div>
      <p class="fig">Figma <b></b></p>
      <p class="hint">Figma 에셋 패널에서 위 세트 이름으로 검색하고 변형(Fill)을 고릅니다. 라이브러리는 <code>OnePlatform-Icon</code>(구 poc-Icon)입니다.</p>
    </div>
  </aside>
</div>
"""


def section(cats, source, sprite):
    n = sum(len(c["icons"]) for c in cats)
    nset = sum(c["sets"] for c in cats)
    catbtns, blocks = [], []
    for c in cats:
        cat = c["category"]
        catbtns.append('<button type="button" data-cat="%s" aria-pressed="false">%s<small>%d</small></button>'
                       % (cat, html.escape(cat), len(c["icons"])))
        cells = []
        for ic in c["icons"]:
            cells.append(
                '<button type="button" class="c" data-cat="%s" data-file="%s" data-set="%s" data-variant="%s" data-fill="%s" data-sz="%d" data-k="%s" title="%s%s">'
                '<svg viewBox="0 0 20 20" aria-hidden="true"><use href="#%s"/></svg><span>%s</span></button>'
                % (cat, html.escape(ic["name"]), html.escape(ic["set"]), html.escape(ic["variant"]), ic["fill"], ic["size"],
                   html.escape("|".join(ic["keywords"])),
                   html.escape(ic["set"]), (" · " + html.escape(ic["variant"])) if ic["variant"] else "",
                   ic["id"], html.escape(ic["name"])))
        blocks.append('<div class="cat" id="cat-%s"><h2>%s<small>세트 %d · 아이콘 %d</small></h2><div class="g">%s</div></div>'
                      % (cat, html.escape(cat), c["sets"], len(c["icons"]), "".join(cells)))
    if source.get("commit"):
        src = "커밋 <code>%s</code> · %s" % (html.escape(source["commit"]), html.escape(source.get("commit_date") or ""))
        if source.get("synced"):
            src += " · %s 동기화" % html.escape(source["synced"])
    else:
        src = "출처 스탬프 없음"
    body = (BODY.replace("{{N}}", str(n)).replace("{{NSET}}", str(nset)).replace("{{NCAT}}", str(len(cats)))
            .replace("{{CATBTNS}}", "\n      ".join(catbtns)).replace("{{CATS}}", "\n    ".join(blocks)))
    out = {"id": "c-Icon", "group": "파운데이션", "nav": "Icon <small>%d</small>" % n, "body": body, "css": CSS.strip(), "js": JS.strip(), "tail": sprite}
    return out, n, nset


def build_zip(cats):
    """svg/ 낱개 + sprite.svg + icons.json 을 cloudx-icons.zip 으로 묶는다.
    타임스탬프를 고정하고 이름순으로 넣어 내용이 같으면 바이트도 같다(CI 재빌드 비교용)."""
    import zipfile
    out = os.path.join(ROOT, "cloudx-icons.zip")
    names = ["sprite.svg", "icons.json", "README.md"] + sorted(ic["file"] for c in cats for ic in c["icons"])
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in names:
            p = os.path.join(ROOT, n)
            if not os.path.exists(p):
                continue
            zi = zipfile.ZipInfo("cloudx-icons/" + n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(p, "rb") as fp:
                z.writestr(zi, fp.read())
    return os.path.getsize(out)


def main():
    sprite_p = os.path.join(ROOT, "sprite.svg")
    if not os.path.exists(sprite_p):
        sys.exit("sprite.svg 가 없습니다 — 먼저 python3 tools/build-sprite.py")
    sprite = read(sprite_p)
    source = load_json("source.json", {})
    cats = collect()
    # 스프라이트와 메타가 어긋나면 멈춘다 — 둘 다 cloudXDS에서 같은 커밋으로 와야 한다
    ids = set(re.findall(r'<symbol id="([^"]+)"', sprite))
    want = set(ic["id"] for c in cats for ic in c["icons"])
    missing, extra = sorted(want - ids), sorted(ids - want)
    if missing or extra:
        sys.exit("스프라이트와 _sets.json이 어긋납니다 — 메타에만 %d · 스프라이트에만 %d\n%s" % (
            len(missing), len(extra), "\n".join(["  - " + m for m in missing[:10]] + ["  + " + e for e in extra[:10]])))

    sec, n, nset = section(cats, source, sprite)
    data = {
        "source": source,
        "count": n,
        "sets": nset,
        "categories": {c["category"]: len(c["icons"]) for c in cats},
        "icons": [ic for c in cats for ic in c["icons"]],
    }
    with open(os.path.join(ROOT, "icons.json"), "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    zkb = build_zip(cats) / 1024
    print("icons.json · cloudx-icons.zip %.0fKB — 아이콘 %d개 · 세트 %d (절은 build-site.py 가 index.html 에 넣는다)" % (zkb, n, nset), file=sys.stderr)


if __name__ == "__main__":
    main()
