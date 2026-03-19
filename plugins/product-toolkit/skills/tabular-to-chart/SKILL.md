---
name: tabular-to-chart
description: "Transform tabular data (Excel/CSV/clipboard) into interactive charts (bar, line, pie, scatter, heatmap, treemap, sankey, funnel) as HTML or Mermaid output. 표 시각화, 차트 생성, 데이터 시각화, 엑셀 차트, CSV 차트가 필요할 때 사용. Use when user mentions chart, visualization, graph, 시각화, 차트, or pastes tabular data."
---

# 테이블 자료 시각화 스킬

Excel/CSV 또는 클립보드 붙여넣기로 주어진 표 데이터를 분석하고 시각화를 구현한다.

**시작 시 안내:** "테이블 시각화 스킬을 적용해 진행합니다."

---

## 0. 환경 점검 (스킬 시작 시 1회)

1. `python3 --version` 또는 `python --version` 실행 (exit code 확인)
2. **성공** → **스크립트 모드**로 진행
3. **실패** → 사용자에게 선택지 제시:
   - **A) 정의 내용만 받고 종료** — Python 설치 없이 직접 생성 모드(HTML)로 차트 제공 후 종료. 필요 시 OS별 설치 링크 안내.
   - **B) Python 설치 후 진행** — 아래 OS별 안내 후 설치 확인, 이후 스크립트 모드로 재진행.
   - **B') Python 자동 설치 시도** — 시스템 설치 명령 실행 시도. 성공 시 스크립트 모드, 실패 시 A와 동일하게 직접 생성 모드.

**OS별 Python 설치 안내 (B 선택 시)**:
- macOS: `brew install python3` 또는 [python.org/downloads](https://www.python.org/downloads/)
- Windows: `winget install Python.Python.3.12` 또는 [python.org/downloads](https://www.python.org/downloads/)
- Linux: `sudo apt install python3` (Debian/Ubuntu) / `sudo dnf install python3` (Fedora)

**의존성:** `parse_tabular.py`·`generate_chart.py`는 Python 표준 라이브러리만 사용. venv 불필요.  
복잡한 xlsx(병합셀·수식) 파싱 시만 openpyxl 필요 — **`run_charts.py` 사용 시 자동 설치됨.**

| | 스크립트 모드 | 직접 생성 모드 |
|--|--------------|---------------|
| **구현** | `scripts/` 실행 | LLM이 HTML/Mermaid 직접 작성 |
| **장점** | 결정적, 토큰 절약, 재사용 가능 | Python 불필요 |

---

## 질문 인터페이스

사용자에게 묻는 모든 질문은 **구조화된 선택지**로 제시한다. 상세 규칙은 `references/question-interface.md` 참조.

---

## 워크플로우

### 1. 입력 수집

- **클립보드 텍스트**: 탭/쉼표 구분으로 파싱. 필요 시 CSV로 저장(UTF-8).
- **파일(Excel/CSV)**: `run_charts.py parse`로 구조 파악.

```bash
python3 scripts/run_charts.py parse --file data.xlsx --summary
python3 scripts/run_charts.py parse --file data.xlsx --list-sheets
python3 scripts/run_charts.py parse --file data.xlsx --sheet "매출" --to-csv output.csv
```

### 2. 구조 파악 + 범위·유형·산출물 한 번에 확인

`--summary` 출력으로 컬럼(이름, 타입, 고유값 수)을 정리하고, **한 번의 질문**으로 아래를 묻는다:

1. **범위**: 전체 데이터 / 특정 영역 집중 / 기타
2. **시각화 유형**: 구조 기반 추천 2~3개 + 이유 제시 (유형 기준: `references/chart-types.md`)
3. **산출물 형태**: 단일 HTML / Mermaid 코드 블록 / 기타

> 유형 선택 후 데이터 매핑(x/y/labels 등)을 간단히 요약하고 확인을 받은 뒤 구현한다.

### 3. 구현

#### A. 스크립트 모드 — HTML

config JSON을 작성하고 실행. **`run_charts.py`를 사용하면 openpyxl 등 의존성이 런타임에 자동 설치된다.**

```bash
python3 scripts/run_charts.py chart --config path/to/chart_config.json
python3 scripts/run_charts.py chart --config path/to/chart_config.json --output result.html
python3 scripts/run_charts.py chart --list-types   # 지원 유형 확인
```

**Config 구조:**
```json
{
  "type": "bar",
  "title": "차트 제목",
  "data_csv": "path/to/data.csv",
  "mapping": { "x": "컬럼A", "y": "컬럼B" }
}
```

클립보드 데이터처럼 CSV 파일이 없는 경우, `data_rows`로 인라인 전달 가능:
```json
{
  "type": "pie",
  "title": "비율",
  "data_rows": [{"항목": "A", "값": "30"}, {"항목": "B", "값": "70"}],
  "mapping": { "labels": "항목", "values": "값" }
}
```

유형별 mapping 키는 `references/chart-types.md` 참조.  
xlsx 입력 시 먼저 `--to-csv`로 변환 후 차트 생성.

#### B. 스크립트 모드 — Mermaid

Mermaid 지원 유형(pie, xychart-beta bar, flowchart)은 LLM이 직접 `.md` 파일로 작성.  
지원 불가 유형(sankey, treemap, heatmap 등)은 HTML로 안내.

#### C. 직접 생성 모드

LLM이 Plotly.js CDN 기반 HTML 또는 Mermaid를 직접 작성.

#### 산출물 위치

입력 파일과 같은 디렉터리가 기본. 사용자 지정 시 그에 따른다.

- CSV: `<dir>/<주제>.csv`
- Config: `<dir>/<주제>_config.json`
- 시각화: `<dir>/<주제>_<유형>.html` 또는 `.md`

### 4. 완료 안내

저장 경로와 데이터 갱신 재사용 방법을 한 줄로 전달.

---

## 스크립트 역할 분리

| 역할 | 담당 |
|------|------|
| 구조 파악, 유형 결정, 매핑 설계 | LLM (이 스킬) |
| 파싱, 수치 집계, HTML 렌더링 | `scripts/` |

```
scripts/
├── run_charts.py          # 진입점 — Python 설치 확인, openpyxl 자동 설치, 서브커맨드 분기
├── parse_tabular.py       # 범용 Excel/CSV 파서
├── generate_chart.py      # 범용 차트 생성기 (JSON config → Plotly HTML)
└── brand_colors.json      # 테마 색상 (선택사항)
```

**파일 생성 시 반드시 `run_charts.py`를 사용한다.** `generate_chart.py` / `parse_tabular.py` 직접 실행도 가능하지만, openpyxl 자동 설치가 필요한 환경에서는 `run_charts.py`를 통해야 한다.

`brand_colors.json`은 선택사항. 없으면 Plotly 기본 팔레트 사용.  
도메인 특화 예시(하나투어 트래픽 등)는 `examples/` 참고.
