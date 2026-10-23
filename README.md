# Cloud X Icons

Cloud X 디자인시스템 아이콘 **487개**(세트 246 · 카테고리 7)를 다른 부서와 공유하기 위한 저장소입니다.

- **보기 · 검색 · 코드 복사**: https://osstemswai.github.io/cloudx-icons/
- **전체 받기**: [`cloudx-icons.zip`](cloudx-icons.zip) — 낱개 SVG 전부 + `sprite.svg` + `icons.json`. 스프라이트만 필요하면 [`sprite.svg`](sprite.svg)

원본은 Figma 라이브러리 **OnePlatform-Icon**(구 poc-Icon)이고, 디자인시스템 저장소 [h1osstem/cloudXDS](https://github.com/h1osstem/cloudXDS)의 `Icon/`에서 정규화한 것을 여기로 그대로 복사합니다. 출처 커밋은 [`meta/source.json`](meta/source.json)에 있습니다. **이 저장소에서 아이콘을 직접 고치지 않습니다.** 추가·수정 요청은 SW디자인팀으로 보내 주세요.

## 쓰는 법

### 1. 스프라이트 한 파일 — 권장

`sprite.svg`를 프로젝트에 두고 `<use>`로 참조합니다. 아이콘 id는 `i-<카테고리>-<이름>`입니다.

```html
<svg class="icon" aria-hidden="true"><use href="sprite.svg#i-00_general-search"/></svg>
```

```css
.icon { width: 20px; height: 20px; color: #1d1d1d; }
```

- **크기는 박스로만** 정합니다. 16 · 20 · 24 중 하나를 씁니다.
- **색은 `color`로** 줍니다. `fill`은 주지 않습니다. 경로에 박힌 `fill="currentColor"`가 우선이라 `fill`은 먹지 않습니다.
- `sprite.svg`는 페이지와 **같은 출처(도메인)** 에 둡니다. 다른 도메인의 파일은 `<use>`가 읽지 못합니다.

### 2. 인라인 SVG

갤러리에서 아이콘을 고르고 「인라인 SVG」 탭을 복사하거나, `svg/` 파일 내용을 그대로 HTML에 넣습니다. React라면 컴포넌트로 감쌉니다. 색은 역시 `color`로 줍니다.

### 3. `<img>`

```html
<img src="svg/00_general/search.svg" width="20" height="20" alt="">
```

가장 간단하지만 **색을 바꿀 수 없습니다**(검정 고정). 어두운 배경에는 맞지 않습니다.

### 4. 목록 데이터

[`icons.json`](icons.json)에 아이콘마다 id · 카테고리 · 세트 · 변형 · 파일 경로 · 그림 크기 · 검색어(한국어 포함)가 들어 있습니다. 아이콘 선택 UI를 만들 때 씁니다.

## 규칙

- 모든 아이콘은 `viewBox="0 0 20 20"`이고 그림이 그 안에 여백을 두고 들어 있습니다. 쓰는 쪽은 박스 크기만 정합니다.
- **선(`Fill=off`)이 기본**이고 면은 이름 뒤에 `-fill`이 붙습니다. `search.svg`가 선, `search-fill.svg`가 면입니다.
- 중립 잉크(검정·진회색)는 `currentColor`입니다. 아이콘 안쪽을 **파낸 흰 조각은 흰색 그대로**라서 어두운 배경에서는 흰색으로 남습니다. 어두운 면에는 선 버전을 쓰세요. 갤러리 상세의 「어두운 면」 미리보기로 확인할 수 있습니다.
- 그림 크기는 **14px(여백 3)과 16px(여백 2)** 두 표준이 섞여 있습니다. 나란히 놓으면 16px 쪽이 커 보입니다. 갤러리 상세의 「그림 Npx」로 확인합니다.

## 카테고리

| 카테고리 | 개수 | 내용 |
|---|---|---|
| `00_arrow` | 66 | 화살표 · 캐럿 · 회전 · 펼침 |
| `00_edit` | 62 | 텍스트 · 그리기 편집 도구 |
| `00_general` | 314 | 일반 |
| `00_modal` | 10 | 모달 피드백 5종(알림 · 확인 · 정보 · 질문 · 경고). 의미색이 고정돼 있습니다 |
| `00_window` | 4 | 창 조작 |
| `01_pms` | 8 | PMS 전용 |
| `01_pms-lnb` | 23 | PMS LNB 환자 배지. 상태 변형(varient·data·other)이라 일반 아이콘과 성격이 다르고, 원본 24px를 20 박스에 축소했습니다 |

## 알아 둘 것 — 원본에서 정리 중인 항목

- 이름 뒤에 **`-2`** 가 붙은 20쌍은 이름만 같고 그림이 다른 아이콘입니다. 화살표의 `up-2` 등은 원형 테두리 안에 든 버전입니다. 이름이 바뀔 수 있으니 id를 하드코딩한 곳을 기억해 두세요.
- `00_modal` 10개와 `empty_state` · `Edit-colorpalette` · `01_pms-lnb` 배지 등 **36개는 색이 고정**되어 `color`를 따르지 않습니다.
- `axial_clipping` · `coronal_clipping` · `sagittal_clipping` · `slice_interval` · `two_view-*` · `thickness-2` 12개는 **반투명 부분**이 있습니다. Figma 렌더와 대조해 디자인 의도임을 확인했습니다(클리핑 평면 표현).
- `empty_state` 2개는 Figma 익스포트가 깨져 그림이 비어 있습니다.

자세한 내용은 cloudXDS의 `Icon/README.md`에 있습니다.

## 저장소 구성

| | |
|---|---|
| `svg/<카테고리>/<이름>.svg` | 낱개 487개. cloudXDS `Icon/svg/` 복제본 |
| `sprite.svg` | 생성물. `<symbol id="i-<카테고리>-<이름>">` 묶음 |
| `index.html` | 생성물. 검색 갤러리(GitHub Pages). 스프라이트를 인라인으로 품고 있어 파일 하나로 동작합니다 |
| `icons.json` | 생성물. 기계용 목록 |
| `cloudx-icons.zip` | 생성물. 낱개 SVG 전부 + sprite.svg + icons.json + README. 갤러리의 「전체 다운로드」가 이 파일입니다 |
| `meta/` | `_sets.json`(세트 · Figma 배치 순서) · `_ink.json`(그림 크기) · `_keywords.json`(한국어 검색어) · `source.json`(출처 스탬프) |
| `tools/` | `sync.py`(cloudXDS에서 복사 + 빌드) · `build-sprite.py` · `build-gallery.py` |

## 갱신 — 관리자용

cloudXDS 클론을 최신으로 받은 뒤 이 저장소에서:

```sh
python3 tools/sync.py ../cloudXDS      # svg/ · meta/ 복사 → sprite.svg → index.html · icons.json
git add -A && git commit -m "동기화 — cloudXDS <커밋>"
```

생성물(`sprite.svg` · `index.html` · `icons.json` · `cloudx-icons.zip`)은 손으로 고치지 않습니다. 갤러리 모양을 바꾸려면 `tools/build-gallery.py`를 고치고 다시 빌드합니다. CI(`.github/workflows/check.yml`)가 다시 빌드해서 커밋과 다르면 막습니다.

---

오스템임플란트 SW디자인 · 사내 공유용
