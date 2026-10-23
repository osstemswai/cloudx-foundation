# Cloud X Foundation

Cloud X 디자인시스템의 기초 자산 — **아이콘 · 컬러 · 넘버 · 타이포그래피** — 를 다른 부서와 공유하는 저장소입니다.

- **보기 · 검색 · 복사**: https://osstemswai.github.io/cloudx-foundation/
- **내려받기**: [`tokens.css`](tokens.css)(컬러·넘버·타이포 변수) · [`tokens.json`](tokens.json)(기계용 목록) · [`cloudx-icons.zip`](cloudx-icons.zip)(아이콘 전부) · [`sprite.svg`](sprite.svg)

원본은 Figma입니다. 토큰·텍스트 스타일은 Cloud-X DS 파일(`dJwm3aKPCcDIGcIwZBhZPS`), 아이콘은 OnePlatform-Icon(구 poc-Icon)에서 읽어 왔고, 기준 날짜는 각 페이지 아래와 [`tokens/`](tokens/) · [`meta/source.json`](meta/source.json)에 있습니다. **이 저장소에서 값이나 아이콘을 직접 고치지 않습니다.** 수정 요청은 SW디자인팀으로 보내 주세요.

## 토큰 쓰는 법 — 컬러 · 넘버 · 타이포그래피

```html
<link rel="stylesheet" href="tokens.css">
```

```css
.card {
  background: var(--color-bg-surface-surface01);
  color: var(--color-fg-neutral-strong);
  padding: var(--number-spacing-x6);
  border-radius: var(--number-radius-lg);
  font: var(--font-weight-regular) var(--font-size-14) / var(--line-height-20) var(--font-family-base);
}
```

- **semantic 토큰을 씁니다.** `color/bg/…` · `color/fg/…` · `number/spacing/…`처럼 역할 이름으로 고릅니다. 팔레트 값(`color/orange/600`)이나 hex·px를 직접 쓰지 않습니다. 값이 바뀌어도 이름은 그대로라 화면이 따라옵니다.
- **이름 규칙**: Figma 변수 이름의 `/`를 `-`로 바꾼 것이 CSS 변수입니다. `color/bg/brand/strong/default` → `--color-bg-brand-strong-default`. 페이지에서 이름을 누르면 `var(--…)`가 복사됩니다.
- **글은 텍스트 스타일로** 고릅니다(`역할/크기/웨이트`, 예: `body/md/regular`). 타이포그래피 페이지의 「CSS 복사」가 `font:` 한 줄을 줍니다. 기본 글꼴은 Pretendard이고 없으면 시스템 산세리프로 대체됩니다.
- `tokens.json`은 같은 토큰에 참조 체인(semantic → primitive)·설명·scopes·텍스트 스타일·이펙트를 더한 목록입니다. 테마 도구나 린트에 쓸 수 있습니다.
- `tokens/component.json`(컴포넌트 내부 토큰 1,300여 개)은 상위 저장소용으로만 두고 CSS·다운로드에는 넣지 않습니다.

## 아이콘 쓰는 법

### 1. 스프라이트 한 파일 — 권장

`sprite.svg`를 프로젝트에 두고 `<use>`로 참조합니다. 아이콘 id는 `i-<카테고리>-<이름>`입니다.

```html
<svg class="icon" aria-hidden="true"><use href="sprite.svg#i-00_general-search"/></svg>
```

```css
.icon { width: 20px; height: 20px; color: var(--color-icon-neutral-strong); }
```

- **크기는 박스로만** 정합니다. 16 · 20 · 24 중 하나를 씁니다.
- **색은 `color`로** 줍니다. `fill`은 주지 않습니다. 경로에 박힌 `fill="currentColor"`가 우선이라 `fill`은 먹지 않습니다.
- `sprite.svg`는 페이지와 **같은 출처(도메인)** 에 둡니다. 다른 도메인의 파일은 `<use>`가 읽지 못합니다.
- 스프라이트를 HTML에 **인라인**할 때는 루트를 `display:none`으로 숨기지 마세요. Chrome이 그 안의 `<mask>`를 버려 excel·pin 같은 아이콘이 덩어리로 나옵니다. `sprite.svg` 루트는 이미 `width="0" height="0" style="position:absolute;overflow:hidden"`이라 그대로 넣으면 됩니다.

### 2. 인라인 SVG

아이콘 페이지에서 아이콘을 고르고 「인라인 SVG」 탭을 복사하거나, `svg/` 파일 내용을 그대로 HTML에 넣습니다. React라면 컴포넌트로 감쌉니다. 색은 역시 `color`로 줍니다.

### 3. `<img>`

```html
<img src="svg/00_general/search.svg" width="20" height="20" alt="">
```

가장 간단하지만 **색을 바꿀 수 없습니다**(검정 고정). 어두운 배경에는 맞지 않습니다.

### 4. 목록 데이터

[`icons.json`](icons.json)에 아이콘마다 id · 카테고리 · 세트 · 변형 · 파일 경로 · 그림 크기 · 검색어(한국어 포함)가 들어 있습니다.

### 아이콘 규칙

- 모든 아이콘은 `viewBox="0 0 20 20"`이고 그림이 그 안에 여백을 두고 들어 있습니다. 쓰는 쪽은 박스 크기만 정합니다.
- **선(`Fill=off`)이 기본**이고 면은 이름 뒤에 `-fill`이 붙습니다. `search.svg`가 선, `search-fill.svg`가 면입니다.
- 중립 잉크(검정·진회색)는 `currentColor`입니다. 아이콘 안쪽을 **파낸 흰 조각은 흰색 그대로**라서 어두운 배경에서는 흰색으로 남습니다. 어두운 면에는 선 버전을 쓰세요.
- 그림 크기는 **14px(여백 3)과 16px(여백 2)** 두 표준이 섞여 있습니다. 상세의 「그림 Npx」로 확인합니다.

| 카테고리 | 개수 | 내용 |
|---|---|---|
| `00_arrow` | 66 | 화살표 · 캐럿 · 회전 · 펼침 |
| `00_edit` | 62 | 텍스트 · 그리기 편집 도구 |
| `00_general` | 314 | 일반 |
| `00_modal` | 10 | 모달 피드백 5종(알림 · 확인 · 정보 · 질문 · 경고). 의미색이 고정돼 있습니다 |
| `00_window` | 4 | 창 조작 |
| `01_pms` | 8 | PMS 전용 |
| `01_pms-lnb` | 23 | PMS LNB 환자 배지. 상태 변형(varient·data·other)이라 일반 아이콘과 성격이 다르고, 원본 24px를 20 박스에 축소했습니다 |

## 알아 둘 것

- **상위 저장소(cloudXDS)와 기준이 다를 수 있습니다.** 토큰은 2026-10-23 Figma에서 직접 읽은 것이고 cloudXDS의 FigmaVariables는 10-13 익스포트입니다. 두 값이 다르면 맞는 쪽은 **최신 Figma**입니다. cloudXDS 재익스포트 때 `tokens/*.json`을 그대로 가져다 쓸 수 있게 같은 스키마로 두었습니다.
- 아이콘 이름 뒤에 **`-2`** 가 붙은 20쌍은 이름만 같고 그림이 다른 아이콘입니다. 이름이 바뀔 수 있으니 id를 하드코딩한 곳을 기억해 두세요.
- `00_modal` 10개와 `empty_state` · `Edit-colorpalette` · `01_pms-lnb` 배지 등 **36개는 색이 고정**되어 `color`를 따르지 않습니다.
- `axial_clipping` · `coronal_clipping` · `sagittal_clipping` · `slice_interval` · `two_view-*` · `thickness-2` 12개는 **반투명 부분**이 있습니다. Figma 렌더와 대조해 디자인 의도임을 확인했습니다.
- `empty_state` 2개는 Figma에서도 빈 벡터라 그림이 없습니다.

## 저장소 구성

| | |
|---|---|
| `index.html` · `icons.html` · `color.html` · `number.html` · `typography.html` | 생성물. GitHub Pages 페이지. 아이콘 페이지는 스프라이트를 인라인으로 품고 있습니다 |
| `tokens.css` · `tokens.json` | 생성물. `tokens/*.json`을 primitive까지 풀어 만든 CSS 변수와 기계용 목록 |
| `tokens/primitive.json` · `semantic.json` · `typography.json` · `component.json` · `styles.json` | Figma 변수·텍스트 스타일·이펙트 덤프(cloudXDS `FigmaVariables/`와 같은 스키마, `styles.json`만 추가). 원본은 Figma |
| `svg/<카테고리>/<이름>.svg` · `sprite.svg` · `icons.json` · `cloudx-icons.zip` | 아이콘 낱개 · 스프라이트(생성물) · 목록(생성물) · 전체 묶음(생성물) |
| `meta/` | 아이콘 세트 순서(`_sets.json`) · 그림 크기(`_ink.json`) · 한국어 검색어(`_keywords.json`) · 출처(`source.json`) |
| `tools/` | `sync.py`(cloudXDS 아이콘 복사 + 전체 빌드) · `build-tokens.py` · `build-sprite.py` · `build-gallery.py` · `build-foundation.py` · `page.py`(공통 셸) |

## 갱신 — 관리자용

**아이콘** — cloudXDS 클론을 최신으로 받은 뒤:

```sh
python3 tools/sync.py ../cloudXDS      # svg/ · meta/ 복사 → 토큰 · 스프라이트 · 페이지 전부 빌드
```

**토큰** — Figma에서 Plugin API로 읽어 `tokens/*.json`을 갱신합니다(변수 컬렉션 4개 · 텍스트 스타일 · 이펙트 스타일, cloudXDS 스키마로 변환). Claude에게 "Figma에서 토큰 다시 읽어줘"라고 하면 수행합니다. 그 뒤:

```sh
python3 tools/build-tokens.py && python3 tools/build-foundation.py
```

생성물은 손으로 고치지 않습니다. 페이지 모양을 바꾸려면 `tools/build-foundation.py` · `build-gallery.py` · `page.py`를 고치고 다시 빌드합니다. CI(`.github/workflows/check.yml`)가 다시 빌드해서 커밋과 다르면 막습니다.

---

오스템임플란트 SW디자인 · 사내 공유용
