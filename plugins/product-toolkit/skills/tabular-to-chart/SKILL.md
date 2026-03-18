---
name: tabular-to-chart
description: "Transform tabular data (Excel/CSV/clipboard) into interactive charts (bar, line, pie, scatter, heatmap, treemap, sankey, funnel) as HTML or Mermaid output. 표 시각화, 차트 생성, 데이터 시각화, 엑셀 차트, CSV 차트가 필요할 때 사용. Use when user mentions chart, visualization, graph, 시각화, 차트, or pastes tabular data."
---

# 테이블 자료 시각화 스킬

Excel/CSV 또는 클립보드 붙여넣기로 주어진 표 형태 데이터를 분석하고, 데이터 구조에 맞는 시각화를 설계·구현한다.

**시작 시 안내:** "테이블 시각화 스킬을 적용해 진행합니다."

---

## 0. 환경 점검 (스킬 시작 시 1회)

워크플로우 진입 전에 Python 사용 가능 여부를 확인한다.

**점검 순서:**
1. `python3 --version` (macOS/Linux) 또는 `python --version` (Windows) 실행
2. 정상 출력이면 → **스크립트 모드**. 이후 재점검하지 않는다.
3. 실패 시 → 선택지 제시:
   - **Python 설치 후 진행** — OS별 안내 제공 후 스크립트 모드
   - **설치 없이 진행** — LLM이 직접 생성하는 **직접 생성 모드**
   - **기타 (직접 입력)**

**스크립트 의존성:**
- `parse_tabular.py`(CSV 파싱)와 `generate_chart.py`는 **Python 표준 라이브러리만** 사용. venv 불필요.
- xlsx 파싱도 stdlib로 시도하며, 병합셀·수식 등 복잡한 구조에서만 openpyxl 폴백이 필요하다.
- openpyxl이 필요한 경우에만 venv 생성을 안내:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate   # Windows: .venv\Scripts\activate
  pip install openpyxl
  ```

### 모드별 동작 차이

| | 스크립트 모드 | 직접 생성 모드 |
|--|--------------|---------------|
| **구현 방식** | `scripts/` 실행 | LLM이 HTML/Mermaid 직접 작성 |
| **장점** | 결정적 실행, 토큰 절약, 재현성 | Python 의존성 없음 |
| **제한** | Python 3.x 필요 | 토큰 소모 큼, 복잡한 차트 품질 차이 가능 |

---

## 질문 인터페이스

모든 단계에서 사용자에게 묻는 질문은 **구조화된 선택지**로 제시한다. 상세 규칙과 도구 우선순위는 `references/question-interface.md` 참조.

---

## 워크플로우

### 1. 입력 정리

- **클립보드**: 탭/쉼표 구분 텍스트로 파싱. 첫 행을 헤더로, 빈 셀·합계 행·반복 헤더는 규칙을 정해 처리. 필요 시 원본 파일과 같은 디렉터리 또는 사용자가 지정한 경로에 CSV로 저장(UTF-8).
- **파일(Excel/CSV)**: `parse_tabular.py`로 구조 파악.
  ```bash
  # 구조 요약
  python3 scripts/parse_tabular.py --file data.xlsx --summary

  # xlsx 시트 목록
  python3 scripts/parse_tabular.py --file data.xlsx --list-sheets

  # 특정 시트를 CSV로 변환 (출력 경로는 자유)
  python3 scripts/parse_tabular.py --file data.xlsx --sheet "매출" --to-csv output.csv
  ```
- xlsx 파싱은 stdlib을 먼저 시도하고, 실패 시 openpyxl을 시도. openpyxl이 없으면 설치 안내 또는 수동 CSV 변환 선택지를 제시한다.

### 2. 구조 파악

`parse_tabular.py --summary` 출력을 기반으로 다음을 정리한다.

| 항목 | 확인 내용 |
|------|-----------|
| **컬럼 목록** | 이름, 추론 타입(numeric/text/date/percentage), 고유값 수 |
| **차원(축)** | 범주형 컬럼 (text, 고유값 적음) |
| **지표** | 수치형 컬럼 (numeric, percentage) |
| **시계열** | 날짜 컬럼 유무 |
| **계층/흐름** | 상위→하위 관계, 순차 단계가 있는지 |

### 2.5 범위 문의 (필수)

데이터 전체를 시각화할지, 특정 영역만 집중할지 선택지로 문의한다.

- **전체 데이터**: 모든 행/컬럼 포함
- **특정 영역 집중**: 필터 조건 지정 (예: 특정 카테고리, 기간 등)
- **기타 (직접 입력)**

### 3. 시각화 유형 제안 및 사용자 확인

데이터 구조를 기반으로 적합한 유형을 **이유와 함께** 제안한다. 유형 후보와 선택 기준은 `references/chart-types.md` 참조.

**확인 절차:**
1. 적합한 유형을 이유와 함께 제안 → 선택지로 수락/변경 문의
2. 유형이 여러 개 적합하면 후보 2~3개를 선택지로 나열
3. **확정 전에는 구현하지 않는다**

### 3.5 산출물 형태 문의 (필수)

- **단일 HTML**: CDN 기반 인터랙티브 차트
- **Mermaid**: 문서(.md) 또는 코드 블록
- **기타 (직접 입력)**: 이미지, JSON 등

### 4. 시각화 설계

확정된 범위·유형·산출물 형태를 기준으로, 구현 전에 다음을 정리한다.

- **데이터 매핑**: 어떤 컬럼을 x/y/labels/values/source/target 등에 매핑할지
- **필터/집계**: 필요한 전처리 (그룹핑, 합산, 정렬 등)
- **인터랙션**: 호버 툴팁, 클릭 상세 등에 표시할 지표
- **출력물**: 확정된 산출물 형태

**사용자 확인을 받은 뒤** 구현 단계로 넘어간다.

### 5. 구현 (요청 시)

#### A. 스크립트 모드 (HTML 산출물)

LLM이 설계(4단계)를 기반으로 config JSON을 작성하고, `generate_chart.py`를 실행한다.

```bash
# config JSON 작성 후 실행
python3 scripts/generate_chart.py --config path/to/chart_config.json

# 지원 차트 유형 확인
python3 scripts/generate_chart.py --list-types
```

**Config JSON 구조:**
```json
{
  "type": "bar",
  "title": "차트 제목",
  "data_csv": "path/to/data.csv",
  "mapping": { "x": "컬럼A", "y": "컬럼B" }
}
```

유형별 mapping 키는 `references/chart-types.md` 참조.

xlsx 데이터인 경우, 먼저 `parse_tabular.py --to-csv`로 CSV 변환 후 차트를 생성한다.

#### A-2. Mermaid 산출물

Mermaid를 선택한 경우, `generate_chart.py`는 사용하지 않는다. LLM이 설계(4단계)를 기반으로 Mermaid 코드 블록을 직접 작성하여 `.md` 파일로 저장한다. Mermaid가 지원하는 유형(pie, bar(xychart-beta), flowchart 등)만 해당하며, 지원하지 않는 유형(sankey, treemap, heatmap 등)은 HTML 산출물로 안내한다.

#### B. 직접 생성 모드 (Python 없음)

LLM이 Plotly.js CDN을 사용하여 HTML을 직접 작성하거나, Mermaid 코드 블록을 직접 작성한다. `scripts/generate_chart.py`의 생성 함수를 참고하여 동일 품질을 유지한다.

#### 산출물 위치

산출물은 **입력 파일과 같은 디렉터리**에 저장하는 것을 기본으로 하되, 사용자가 다른 경로를 지정하면 그에 따른다.

- CSV: `<입력파일 디렉터리>/<주제>.csv`
- Config: `<입력파일 디렉터리>/<주제>_config.json`
- 시각화: `<입력파일 디렉터리>/<주제>_<유형>.html` 또는 `.md`

### 6. 완료 시 안내

저장한 파일 경로와 사용법 요약을 한 줄로 전달. 데이터 갱신 재사용 방법이 있으면 짧게 안내.

---

## 스크립트 연동 (역할 분리)

| 역할 | 담당 |
|------|------|
| 구조 파악, 차트 유형 결정, 매핑 설계 | LLM (이 스킬) |
| 파일 파싱, 수치 집계, HTML 렌더링 | `scripts/` |

```
scripts/
├── parse_tabular.py       # 범용 Excel/CSV 파서 (xlsx: stdlib → openpyxl 폴백)
├── generate_chart.py      # 범용 차트 생성기 (JSON config → Plotly HTML)
└── brand_colors.json      # 테마 색상 (선택사항, 없으면 기본 팔레트 사용)
```

- `brand_colors.json`은 **선택사항**. 있으면 해당 브랜드 컬러를 적용하고, 없으면 Plotly 기본 팔레트를 사용한다.
- 도메인 특화 예시(하나투어 트래픽 등)는 `examples/`에 참고용으로 포함되어 있다.
