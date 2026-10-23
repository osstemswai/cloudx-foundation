#!/usr/bin/env python3
"""Cloud X Foundation 페이지 공통 셸 — 헤더(내비·다운로드·테마) · 기본 CSS · 공통 JS(복사·토스트·테마·검색).

빌더(build-gallery.py · build-foundation.py)가 `render()`로 본문만 끼워 넣습니다.
"""
import html

REPO_URL = "https://github.com/osstemswai/cloudx-foundation"
NAV = [("index.html", "홈"), ("icons.html", "아이콘"), ("color.html", "컬러"), ("number.html", "넘버"), ("typography.html", "타이포그래피")]

BASE_CSS = r"""
:root{--bg:#f5f5f5;--card:#fff;--chip:#e9e9e9;--line:rgba(0,0,0,.1);--ink:#1d1d1d;--ink2:#565656;--ink3:#8a8a8a;
      --accent:#eb6100;--accent-soft:#fef1e9;--accent-line:#f5af7d;--pv:#fff;--pv-line:rgba(0,0,0,.08);--code-bg:#fafafa;color-scheme:light}
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
.hd{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:10px 24px;background:var(--bg);border-bottom:1px solid var(--line)}
.hd h1{margin:0;font-size:17px;letter-spacing:-.01em;display:flex;align-items:center;gap:10px}
.hd h1 a{text-decoration:none}
.hd h1 i{width:22px;height:22px;border-radius:6px;background:var(--accent);display:inline-block}
.nav{display:flex;gap:2px;flex-wrap:wrap}
.nav a{text-decoration:none;font-size:13px;font-weight:600;color:var(--ink3);padding:6px 10px;border-radius:8px}
.nav a:hover{color:var(--ink);background:var(--chip)}
.nav a.on{color:var(--ink);background:var(--chip)}
.hd__acts{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font-size:12.5px;font-weight:600;text-decoration:none;cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn--dark{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn--dark:hover{opacity:.85;color:var(--bg)}
.wrap{padding:24px 24px 60px;max-width:1600px;margin:0 auto}
.pg-h{margin:0 0 6px;font-size:26px;letter-spacing:-.02em}
.pg-sub{margin:0 0 20px;color:var(--ink3);font-size:13px}
.sec{margin:0 0 36px}
.sec h2{font-size:16px;margin:0 0 4px}
.sec .lead{margin:0 0 12px;color:var(--ink3);font-size:13px}
.search{display:flex;align-items:center;gap:10px;height:44px;padding:0 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);cursor:text;max-width:560px;margin:0 0 18px}
.search:focus-within{border-color:var(--ink2)}
.search input{flex:1;min-width:0;border:0;outline:0;background:none;font:inherit;font-size:14px;color:var(--ink)}
.search input::placeholder{color:var(--ink3)}
.search kbd{font:11px ui-monospace,Menlo,monospace;color:var(--ink3);border:1px solid var(--line);border-radius:5px;padding:1px 6px}
.count{font-size:12px;color:var(--ink3);white-space:nowrap}
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
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:200;background:#1f1f1f;color:#fff;font-size:13px;padding:10px 16px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .15s}
.toast.show{opacity:1}
.ft{padding:28px 24px 48px;border-top:1px solid var(--line);font-size:12px;color:var(--ink3);line-height:1.8;max-width:1600px;margin:0 auto}
.ft a{color:var(--ink2)}
@media (max-width:980px){.wrap{padding:16px 16px 48px}.hd{padding:10px 16px}.ft{padding:24px 16px 40px}}
"""

BASE_JS = r"""
(function () {
  var root = document.documentElement;
  try { var t = localStorage.getItem('cxi-theme'); if (t) root.setAttribute('data-theme', t); } catch (e) {}
  var tb = document.getElementById('theme');
  if (tb) tb.addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') === 'dark' || (!root.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark'; root.setAttribute('data-theme', next);
    try { localStorage.setItem('cxi-theme', next); } catch (e) {}
  });
  window.cxToast = function (msg) {
    var t = document.getElementById('toast'); if (!t) return; t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 1300);
  };
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-cp]'); if (!el) return;
    var txt = el.getAttribute('data-cp');
    navigator.clipboard.writeText(txt).then(function () { cxToast('복사했습니다 — ' + txt); }, function () { cxToast('복사에 실패했습니다'); });
  });
  /* 검색 — input[data-filter="<행 선택자>"] : 행의 data-k(소문자) 에 포함되면 보인다. 비는 그룹은 숨긴다 */
  document.querySelectorAll('input[data-filter]').forEach(function (inp) {
    var rows = Array.prototype.slice.call(document.querySelectorAll(inp.getAttribute('data-filter')));
    var cnt = document.querySelector(inp.getAttribute('data-count') || 'x');
    function run() {
      var v = (inp.value || '').trim().toLowerCase(), n = 0;
      rows.forEach(function (r) { var ok = !v || (r.getAttribute('data-k') || '').indexOf(v) >= 0; r.hidden = !ok; if (ok) n++; });
      document.querySelectorAll('[data-group]').forEach(function (g) { g.hidden = !g.querySelector('[data-k]:not([hidden])'); });
      if (cnt) cnt.textContent = n + ' / ' + rows.length;
    }
    inp.addEventListener('input', run); run();
    document.addEventListener('keydown', function (e) { if (e.key === '/' && document.activeElement !== inp) { e.preventDefault(); inp.focus(); } if (e.key === 'Escape' && document.activeElement === inp) { inp.value = ''; run(); inp.blur(); } });
  });
})();
"""

PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css">
<style>{{BASE_CSS}}{{CSS}}</style>
</head>
<body>
<header class="hd">
  <h1><a href="index.html"><i></i></a><a href="index.html">Cloud X Foundation</a></h1>
  <nav class="nav">{{NAV}}</nav>
  <div class="hd__acts">
    {{ACTS}}
    <button type="button" class="btn" id="theme" aria-label="테마 전환">테마</button>
  </div>
</header>
<main class="wrap">
{{BODY}}
</main>
<footer class="ft">
  원본은 Figma 라이브러리입니다 — 토큰·텍스트 스타일은 Cloud-X DS 파일(<code>{{FIGMA}}</code>, {{STAMP}} 기준), 아이콘은 OnePlatform-Icon(구 poc-Icon). 이 사이트는 거기서 읽어 만든 생성물이고 여기서 직접 고치지 않습니다. 수정 요청은 SW디자인팀으로.<br>
  오스템임플란트 SW디자인 · 사내 공유용 · <a href="{{REPO}}" target="_blank" rel="noopener">GitHub</a>
</footer>
<div class="toast" id="toast" role="status"></div>
{{TAIL}}
<script>{{BASE_JS}}{{JS}}</script>
</body>
</html>
"""


def render(title, active, body, css="", js="", tail="", desc="", acts=None, figma="dJwm3aKPCcDIGcIwZBhZPS", stamp=""):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == active else "", t) for h, t in NAV)
    default_acts = ('<a class="btn btn--dark" href="tokens.css" download>tokens.css</a>'
                    '<a class="btn" href="tokens.json" download>tokens.json</a>'
                    '<a class="btn" href="cloudx-icons.zip" download>아이콘 ZIP</a>')
    return (PAGE.replace("{{TITLE}}", html.escape(title)).replace("{{DESC}}", html.escape(desc)).replace("{{BASE_CSS}}", BASE_CSS)
            .replace("{{CSS}}", css).replace("{{NAV}}", nav).replace("{{ACTS}}", acts if acts is not None else default_acts)
            .replace("{{BODY}}", body).replace("{{FIGMA}}", figma).replace("{{STAMP}}", html.escape(stamp)).replace("{{REPO}}", REPO_URL)
            .replace("{{TAIL}}", tail).replace("{{BASE_JS}}", BASE_JS.strip()).replace("{{JS}}", js))
