#!/usr/bin/env python3
"""Cloud X Foundation 한 페이지 앱 셸 — 왼쪽 LNB · 해시로 절 전환(`#c-Icon`) · 오른쪽 목차 · 테마 · 복사 · 검색.

스토리북(cloudXDS)과 같은 구조입니다. 빌더(build-site.py)가 절(section) 목록을 넘기면 index.html 한 장을 냅니다.
절 하나 = {"id": "c-Icon", "group": "파운데이션", "nav": "Icon (487)", "body": html, "css": "", "js": "", "tail": ""}
"""
import html

REPO_URL = "https://github.com/osstemswai/cloudx-foundation"
FIGMA = "dJwm3aKPCcDIGcIwZBhZPS"

BASE_CSS = r"""
:root{--bg:#f5f5f5;--side:#ededed;--card:#fafafa;--chip:#e9e9e9;--line:rgba(0,0,0,.1);--hover:rgba(209,209,209,.5);--ink:#1d1d1d;--ink2:#565656;--ink3:#8a8a8a;
      --accent:#eb6100;--accent-soft:#fef1e9;--accent-line:#f5af7d;--pv:#fff;--pv-line:rgba(0,0,0,.08);--code-bg:#fafafa;color-scheme:light}
:root[data-theme="dark"]{--bg:#121212;--side:#161616;--card:#191919;--chip:#262626;--line:rgba(102,102,102,.28);--hover:rgba(104,104,104,.3);--ink:#ebebeb;--ink2:#c4c4c4;--ink3:#8f8f8f;
      --accent:#f08a3e;--accent-soft:rgba(235,97,0,.18);--accent-line:#b85a16;--pv:#f3f4f5;--pv-line:transparent;--code-bg:#0d0d0d;color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121212;--side:#161616;--card:#191919;--chip:#262626;--line:rgba(102,102,102,.28);--hover:rgba(104,104,104,.3);
      --ink:#ebebeb;--ink2:#c4c4c4;--ink3:#8f8f8f;--accent:#f08a3e;--accent-soft:rgba(235,97,0,.18);--accent-line:#b85a16;--pv:#f3f4f5;--pv-line:transparent;--code-bg:#0d0d0d;color-scheme:dark}}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink)}
body{font:15px/1.6 Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
button{font:inherit;color:inherit}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{scrollbar-width:thin;scrollbar-color:var(--line) transparent}
::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-thumb{background:var(--line);border-radius:8px}

/* ── 뼈대: LNB 262 · 본문 · 목차 210 (스토리북과 같은 치수) ── */
.sb-wrap{display:grid;grid-template-columns:262px minmax(0,1fr);min-height:100vh;max-width:1480px;margin:0 auto}
.sb-nav{position:sticky;top:0;height:100vh;overflow:auto;border-right:1px solid var(--line);padding:22px 0 72px;background:var(--side);scrollbar-width:none}
.sb-nav::-webkit-scrollbar{width:0;height:0}
.sb-brand{padding:0 20px 14px}
.sb-brand h1{font-size:15px;margin:0;letter-spacing:-.02em;display:flex;align-items:center;gap:8px}
.sb-brand h1 i{width:16px;height:16px;border-radius:4px;background:var(--accent);display:inline-block}
.sb-brand p{font-size:11.5px;color:var(--ink3);margin:5px 0 0;line-height:1.6}
.sb-group{font-size:11px;font-weight:700;color:var(--ink3);margin:18px 20px 6px;letter-spacing:.04em}
.sb-nav a{display:block;margin:0 10px;padding:6px 10px;font-size:13.5px;color:var(--ink2);border-radius:6px;text-decoration:none}
.sb-nav a:hover{background:var(--hover);color:var(--ink)}
.sb-nav a.on{background:var(--hover);color:var(--ink);font-weight:600}
.sb-nav a small{color:var(--ink3);font-weight:400;margin-left:4px}
.sb-nav a.dl::after{content:"↓";float:right;color:var(--ink3)}
.sb-theme{position:fixed;left:180px;bottom:14px;z-index:40;display:flex;border:1px solid var(--line);border-radius:999px;padding:2px;background:var(--side)}
.sb-theme button{width:30px;height:24px;border:0;border-radius:999px;background:none;color:var(--ink3);cursor:pointer;font-size:12px}
.sb-theme button.on{background:var(--hover);color:var(--ink)}
.sb-main{display:grid;grid-template-columns:minmax(0,1100px) 210px;gap:56px;padding:48px 40px 120px;align-items:start;justify-content:center}
.sb-comp{scroll-margin-top:24px;padding-top:4px;min-width:0}
.sb-comp[hidden]{display:none}
.sb-comp>h2{font-size:40px;line-height:1.15;margin:0 0 10px;letter-spacing:-.035em}
.sb-sub{font-size:14px;color:var(--ink3);margin:0 0 26px}
.sb-h3{font-size:22px;margin:40px 0 6px;letter-spacing:-.01em}
.sb-h4{font-size:15px;margin:24px 0 8px}
.sb-h4 small{margin-left:8px;color:var(--ink3);font-weight:400;font-size:12px}
.sb-h3 small{margin-left:8px;color:var(--ink3);font-weight:400;font-size:12px}
.sb-h3:first-of-type{margin-top:8px}
.lead{margin:0 0 14px;color:var(--ink3);font-size:13.5px}
.sb-toc{position:sticky;top:44px;max-height:calc(100vh - 88px);overflow:auto;scrollbar-width:none;font-size:12.5px;border-left:1px solid var(--line);padding-left:16px}
.sb-toc::-webkit-scrollbar{width:0;height:0}
.sb-toc b{display:block;font-size:11px;color:var(--ink3);font-weight:700;margin-bottom:9px;letter-spacing:.06em;text-transform:uppercase}
.sb-toc a{display:block;color:var(--ink3);text-decoration:none;padding:3px 0;line-height:1.5}
.sb-toc a:hover{color:var(--ink)}
.sb-toc a.on{color:var(--accent);font-weight:600}
.sb-toc a.lv3{padding-left:10px;font-size:12px}
.btn{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font-size:12.5px;font-weight:600;text-decoration:none;cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn--dark{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn--dark:hover{opacity:.85;color:var(--bg)}
.search{display:flex;align-items:center;gap:10px;height:44px;padding:0 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);cursor:text;max-width:560px;margin:0 0 18px}
.search:focus-within{border-color:var(--ink2)}
.search input{flex:1;min-width:0;border:0;outline:0;background:none;font:inherit;font-size:14px;color:var(--ink)}
.search input::placeholder{color:var(--ink3)}
.search kbd{font:11px ui-monospace,Menlo,monospace;color:var(--ink3);border:1px solid var(--line);border-radius:5px;padding:1px 6px}
.count{font-size:12px;color:var(--ink3);white-space:nowrap}
.tw{overflow-x:auto}
table.t{width:100%;border-collapse:collapse;font-size:13px}
table.t th{text-align:left;font-size:11.5px;color:var(--ink3);font-weight:600;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
table.t td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
table.t tr[hidden]{display:none}
table.t code{font-size:12px}
.cp{cursor:pointer;border:1px solid transparent;border-radius:6px;padding:2px 6px;margin:-2px -6px}
.cp:hover{border-color:var(--line);background:var(--chip)}
.sw{display:inline-block;width:28px;height:28px;border-radius:7px;border:1px solid var(--pv-line);vertical-align:middle;
    background-image:linear-gradient(45deg,#ccc 25%,transparent 25%),linear-gradient(-45deg,#ccc 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ccc 75%),linear-gradient(-45deg,transparent 75%,#ccc 75%);background-size:8px 8px;background-position:0 0,0 4px,4px -4px,-4px 0}
.sw i{display:block;width:100%;height:100%;border-radius:6px}
.mut{color:var(--ink3);font-size:12px}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:200;background:#1f1f1f;color:#fff;font-size:13px;padding:10px 16px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .15s}
.toast.show{opacity:1}
@media (max-width:1180px){.sb-main{grid-template-columns:minmax(0,1fr)}.sb-toc{display:none}}
@media (max-width:980px){
  .sb-wrap{grid-template-columns:1fr}
  .sb-nav{position:sticky;top:0;height:auto;max-height:none;overflow-x:auto;overflow-y:hidden;border-right:0;border-bottom:1px solid var(--line);padding:10px 8px;display:flex;align-items:center;gap:2px;white-space:nowrap;z-index:30}
  .sb-brand{padding:0 10px 0 6px}.sb-brand p{display:none}
  .sb-group{margin:0 4px 0 10px}
  .sb-nav a{margin:0 2px;padding:6px 9px}
  .sb-theme{left:auto;right:14px}
  .sb-main{padding:20px 16px 60px;gap:0}
}
"""

BASE_JS = r"""
(function () {
  var root = document.documentElement;
  function applyTheme(t) { if (t) root.setAttribute('data-theme', t); document.querySelectorAll('.sb-theme button').forEach(function (b) {
    var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); b.classList.toggle('on', b.dataset.t === cur); }); }
  try { applyTheme(localStorage.getItem('cxi-theme')); } catch (e) { applyTheme(null); }
  document.querySelectorAll('.sb-theme button').forEach(function (b) { b.addEventListener('click', function () {
    applyTheme(b.dataset.t); try { localStorage.setItem('cxi-theme', b.dataset.t); } catch (e) {} }); });
  window.cxToast = function (msg) { var t = document.getElementById('toast'); if (!t) return; t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 1300); };
  document.addEventListener('click', function (e) { var el = e.target.closest('[data-cp]'); if (!el) return; var txt = el.getAttribute('data-cp');
    navigator.clipboard.writeText(txt).then(function () { cxToast('복사했습니다 — ' + txt); }, function () { cxToast('복사에 실패했습니다'); }); });
  /* 검색 — input[data-filter="<행 선택자>"] 는 자기 절(.sb-comp) 안에서만 거른다 */
  document.querySelectorAll('input[data-filter]').forEach(function (inp) {
    var sec = inp.closest('.sb-comp'); var rows = Array.prototype.slice.call(sec.querySelectorAll(inp.getAttribute('data-filter')));
    var cnt = sec.querySelector(inp.getAttribute('data-count') || 'x');
    function run() { var v = (inp.value || '').trim().toLowerCase(), n = 0;
      rows.forEach(function (r) { var ok = !v || (r.getAttribute('data-k') || '').indexOf(v) >= 0; r.hidden = !ok; if (ok) n++; });
      sec.querySelectorAll('[data-group]').forEach(function (g) { g.hidden = !g.querySelector('[data-k]:not([hidden])'); });
      if (cnt) cnt.textContent = n + ' / ' + rows.length; }
    inp.addEventListener('input', run); run();
    inp.addEventListener('keydown', function (e) { if (e.key === 'Escape') { inp.value = ''; run(); inp.blur(); } });
  });
  document.addEventListener('keydown', function (e) { if (e.key !== '/' || /input|textarea/i.test(document.activeElement.tagName)) return;
    var sec = document.querySelector('.sb-comp:not([hidden])'); var inp = sec && sec.querySelector('input[data-filter], input#q'); if (inp) { e.preventDefault(); inp.focus(); } });
  /* 절 전환 — #c-Icon · #c-Icon?icon=… */
  var pages = Array.prototype.slice.call(document.querySelectorAll('.sb-comp')), toc = document.getElementById('sb-toc');
  function buildToc(sec) { if (!toc) return; toc.innerHTML = ''; if (!sec) return;
    var b = document.createElement('b'); b.textContent = 'On this page'; toc.appendChild(b);
    sec.querySelectorAll('h3.sb-h3, h4.sb-h4').forEach(function (h, i) { if (!h.id) h.id = sec.id + '-h' + i;
      var a = document.createElement('a'); a.href = '#' + h.id; a.className = h.tagName === 'H4' ? 'lv3' : ''; a.textContent = h.firstChild ? h.firstChild.textContent.trim() : h.textContent.trim(); toc.appendChild(a); }); }
  function show(id, push) { var target = pages.find(function (p) { return p.id === id; }) || pages[0]; if (!target) return;
    pages.forEach(function (p) { p.hidden = p !== target; });
    document.querySelectorAll('.sb-nav a[href^="#"]').forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + target.id); });
    buildToc(target); if (push && location.hash.split('?')[0] !== '#' + target.id) history.pushState(null, '', '#' + target.id);
    window.scrollTo(0, 0); }
  function route() { var raw = location.hash.slice(1); var id = raw.split('?')[0];
    if (/^icon=/.test(raw)) { location.replace('#c-Icon?' + raw); return; }           /* 옛 딥링크 #icon=… */
    var sec = pages.find(function (p) { return p.id === id; });
    if (!sec) { var h = id && document.getElementById(id); if (h) { var owner = h.closest('.sb-comp'); if (owner) { show(owner.id, false); h.scrollIntoView({ block: 'start' }); return; } } }
    show(id || (pages[0] && pages[0].id), false); if (window.icSelectFromHash) icSelectFromHash(); }
  document.addEventListener('click', function (e) { var a = e.target.closest('.sb-nav a[href^="#"]'); if (!a) return; var id = a.getAttribute('href').slice(1);
    if (pages.some(function (p) { return p.id === id; })) { e.preventDefault(); show(id, true); } });
  window.addEventListener('hashchange', route); route();
})();
"""

PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cloud X Foundation</title>
<meta name="description" content="Cloud X 디자인시스템 기초 자산 — 아이콘 · 컬러 · 넘버 · 타이포그래피">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css">
<style>{{BASE_CSS}}{{CSS}}</style>
</head>
<body>
<div class="sb-wrap">
<nav class="sb-nav">
  <div class="sb-brand"><h1><i></i>Cloud X Foundation</h1><p>Figma {{STAMP}} 기준 · {{COUNTS}}</p></div>
  {{NAV}}
  <div class="sb-group">내려받기</div>
  <a class="dl" href="tokens.css" download>tokens.css</a>
  <a class="dl" href="cloudx-icons.zip" download>아이콘 ZIP</a>
</nav>
<main class="sb-main">
<div class="sb-pages">
{{SECTIONS}}
</div>
<aside class="sb-toc" id="sb-toc"></aside>
</main>
</div>
<div class="sb-theme" role="group" aria-label="테마"><button type="button" data-t="light" title="라이트">☀</button><button type="button" data-t="dark" title="다크">☾</button></div>
<div class="toast" id="toast" role="status"></div>
{{TAIL}}
<script>{{JS}}
{{BASE_JS}}</script>
</body>
</html>
"""


def render_app(sections, stamp="", counts=""):
    groups = []
    for s in sections:
        if not groups or groups[-1][0] != s["group"]:
            groups.append((s["group"], []))
        groups[-1][1].append(s)
    nav = "".join('<div class="sb-group">%s</div>%s' % (html.escape(g), "".join('<a href="#%s">%s</a>' % (s["id"], s["nav"]) for s in items)) for g, items in groups)
    secs = "".join('<section class="sb-comp" id="%s" hidden>%s</section>\n' % (s["id"], s["body"]) for s in sections)
    css = "".join(s.get("css", "") for s in sections)
    js = "".join(s.get("js", "") for s in sections)
    tail = "".join(s.get("tail", "") for s in sections)
    return (PAGE.replace("{{BASE_CSS}}", BASE_CSS).replace("{{CSS}}", css).replace("{{NAV}}", nav).replace("{{SECTIONS}}", secs)
            .replace("{{STAMP}}", html.escape(stamp)).replace("{{COUNTS}}", html.escape(counts)).replace("{{FIGMA}}", FIGMA).replace("{{REPO}}", REPO_URL)
            .replace("{{TAIL}}", tail).replace("{{BASE_JS}}", BASE_JS.strip()).replace("{{JS}}", js))
