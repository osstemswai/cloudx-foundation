#!/usr/bin/env python3
"""meta/ + sprite.svg → index.html (검색 갤러리) · icons.json (기계용 목록).

    python3 tools/build-gallery.py

index.html은 스프라이트를 인라인으로 품고 있어 파일 하나로 동작합니다(GitHub Pages).
세트 순서는 Figma 캔버스 배치 순서(`meta/_sets.json`), 그림 크기는 `meta/_ink.json`,
한국어 검색어는 `meta/_keywords.json`에서 옵니다. 셋 다 cloudXDS에서 복사해 온 것이고
`tools/sync.py`가 갱신합니다.
"""
import os, re, json, html, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
META = os.path.join(ROOT, "meta")
REPO_URL = "https://github.com/osstemswai/cloudx-icons"


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
:root{--bg:#f5f5f5;--card:#fff;--chip:#e9e9e9;--line:rgba(0,0,0,.1);--ink:#1d1d1d;--ink2:#565656;--ink3:#8a8a8a;
      --accent:#eb6100;--accent-soft:#fef1e9;--accent-line:#f5af7d;--pv:#fff;--pv-line:rgba(0,0,0,.08);--pv-dark:#1d1d1d;
      --code-bg:#fafafa;color-scheme:light}
:root[data-theme="dark"]{--bg:#121212;--card:#191919;--chip:#262626;--line:rgba(102,102,102,.28);--ink:#ebebeb;--ink2:#c4c4c4;--ink3:#8f8f8f;
      --accent:#f08a3e;--accent-soft:rgba(235,97,0,.18);--accent-line:#b85a16;--pv:#f3f4f5;--pv-line:transparent;--code-bg:#0d0d0d;color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121212;--card:#191919;--chip:#262626;--line:rgba(102,102,102,.28);
      --ink:#ebebeb;--ink2:#c4c4c4;--ink3:#8f8f8f;--accent:#f08a3e;--accent-soft:rgba(235,97,0,.18);--accent-line:#b85a16;--pv:#f3f4f5;--pv-line:transparent;--code-bg:#0d0d0d;color-scheme:dark}}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink)}
body{font:14px/1.5 Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
button{font:inherit;color:inherit}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{scrollbar-width:thin;scrollbar-color:var(--line) transparent}
::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-thumb{background:var(--line);border-radius:8px}

.hd{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:12px 24px;background:var(--bg);border-bottom:1px solid var(--line)}
.hd h1{margin:0;font-size:17px;letter-spacing:-.01em;display:flex;align-items:center;gap:10px}
.hd h1 svg{width:22px;height:22px;color:var(--accent)}
.hd__n{font-size:12.5px;color:var(--ink3)}
.hd__acts{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font-size:12.5px;font-weight:600;text-decoration:none;cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn--dark{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn--dark:hover{opacity:.85;color:var(--bg)}
.btn svg{width:14px;height:14px}

.wrap{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:28px;align-items:start;padding:20px 24px 60px;max-width:1600px;margin:0 auto}
.search{display:flex;align-items:center;gap:10px;height:48px;padding:0 16px;border:1px solid var(--line);border-radius:12px;background:var(--card);cursor:text}
.search:focus-within{border-color:var(--ink2)}
.search svg{width:18px;height:18px;color:var(--ink3);flex:none}
.search input{flex:1;min-width:0;border:0;outline:0;background:none;font:inherit;font-size:15px;color:var(--ink)}
.search input::placeholder{color:var(--ink3)}
.search kbd{font:11px ui-monospace,Menlo,monospace;color:var(--ink3);border:1px solid var(--line);border-radius:5px;padding:1px 6px}
.tools{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:12px 0 4px}
.seg{display:inline-flex;background:var(--chip);border-radius:999px;padding:3px}
.seg button{border:0;background:none;font-size:12.5px;font-weight:600;color:var(--ink3);padding:6px 14px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--card);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.count{font-size:12px;color:var(--ink3);white-space:nowrap}
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

.d{position:sticky;top:76px;border:1px solid var(--line);border-radius:14px;background:var(--card);padding:20px;max-height:calc(100vh - 96px);overflow:auto}
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
.pv .k{background:#1d1d1d;color:#ebebeb}
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

.ft{padding:28px 24px 48px;border-top:1px solid var(--line);font-size:12px;color:var(--ink3);line-height:1.8;max-width:1600px;margin:0 auto}
.ft a{color:var(--ink2)}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:200;background:#1f1f1f;color:#fff;font-size:13px;padding:10px 16px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .15s}
.toast.show{opacity:1}
.d__head{display:flex;align-items:flex-start;gap:10px}
.d__head .d__name{flex:1;min-width:0}
.d__close{display:none;flex:none;width:30px;height:30px;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;background:var(--card);cursor:pointer;padding:0}
.d__close svg{width:14px;height:14px}
@media (max-width:980px){
  .wrap{grid-template-columns:1fr;padding:16px 16px 48px}
  .hd{padding:10px 16px}.ft{padding:24px 16px 40px}
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

  /* 테마 — 시스템 설정을 따르고, 버튼으로 바꾸면 이 브라우저에만 기억한다 */
  var root = document.documentElement;
  try { var t = localStorage.getItem('cxi-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}
  $('#theme').addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') === 'dark' || (!root.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('cxi-theme', next); } catch (e) {}
  });

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
    if (remember) history.replaceState(null, '', '#icon=' + a.cat + '/' + encodeURIComponent(a.file));
  }
  function close() {
    d.classList.remove('open');
    if (cur) { cur.classList.remove('on'); cur = null; }
    history.replaceState(null, '', location.pathname + location.search);
  }
  function toast(msg) {
    var t = $('#toast'); t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 1300);
  }
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

  /* 딥링크 — #icon=<카테고리>/<파일> */
  var m = /[#&]icon=([^&/]+)\/([^&]+)/.exec(location.hash);
  if (m) {
    var file = decodeURIComponent(m[2]);
    var hit = cells.filter(function (x) { return x.dataset.cat === m[1] && x.dataset.file === file; })[0];
    if (hit) { select(hit, false); hit.scrollIntoView({ block: 'center' }); }
  }
})();
"""

PAGE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cloud X Icons</title>
<meta name="description" content="Cloud X 디자인시스템 아이콘 {{N}}개 — 검색하고 코드를 복사하거나 SVG를 내려받습니다.">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css">
<style>{{CSS}}</style>
</head>
<body>
<header class="hd">
  <h1><svg viewBox="0 0 20 20" aria-hidden="true"><use href="#i-00_general-shapes-fill"/></svg>Cloud X Icons</h1>
  <span class="hd__n">아이콘 {{N}} · 세트 {{NSET}} · 카테고리 {{NCAT}}</span>
  <div class="hd__acts">
    <a class="btn btn--dark" href="sprite.svg" download>sprite.svg 내려받기</a>
    <a class="btn" href="{{REPO}}/archive/refs/heads/main.zip">전체 ZIP</a>
    <a class="btn" href="{{REPO}}" target="_blank" rel="noopener">GitHub</a>
    <button type="button" class="btn" id="theme" aria-label="테마 전환">테마</button>
  </div>
</header>

<main class="wrap">
  <section>
    <label class="search"><svg viewBox="0 0 20 20" aria-hidden="true"><use href="#i-00_general-search"/></svg>
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
</main>

<footer class="ft">
  원본은 Figma 라이브러리 <b>OnePlatform-Icon</b>(구 poc-Icon)이고, <a href="https://github.com/h1osstem/cloudXDS" target="_blank" rel="noopener">h1osstem/cloudXDS</a>의 <code>Icon/</code>에서 정규화한 것을 이 저장소가 그대로 가져옵니다
  ({{SOURCE}}). 아이콘을 고칠 일이 있으면 디자인시스템 담당자에게 요청해 주세요. 이 저장소에서 직접 고치지 않습니다.<br>
  오스템임플란트 SW디자인 · 사내 공유용
</footer>
<div class="toast" id="toast" role="status"></div>
{{SPRITE}}
<script>{{JS}}</script>
</body>
</html>
"""


def render(cats, source, sprite):
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
    page = (PAGE.replace("{{CSS}}", CSS.strip()).replace("{{JS}}", JS.strip())
            .replace("{{N}}", str(n)).replace("{{NSET}}", str(nset)).replace("{{NCAT}}", str(len(cats)))
            .replace("{{REPO}}", REPO_URL).replace("{{CATBTNS}}", "\n      ".join(catbtns))
            .replace("{{CATS}}", "\n    ".join(blocks)).replace("{{SOURCE}}", src).replace("{{SPRITE}}", sprite))
    return page, n, nset


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

    page, n, nset = render(cats, source, sprite)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(page)
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
    print("index.html — 아이콘 %d개 · 세트 %d · %.0fKB / icons.json" % (n, nset, len(page) / 1024), file=sys.stderr)


if __name__ == "__main__":
    main()
