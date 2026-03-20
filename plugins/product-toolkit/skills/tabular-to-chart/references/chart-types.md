# 시각화 유형 가이드

## 유형 선택 기준

| 데이터 특성 | 추천 유형 | 주의 |
|-------------|-----------|------|
| 범주별 수치 비교 | **bar** | 항목 수 ≤ 20 |
| 범주별 수치 + 그룹 | **bar** (color 컬럼) | grouped 자동 |
| 누적 비교 | **stacked_bar** | color 컬럼 필수 |
| 시계열 추이 | **line** | y에 복수 컬럼 가능 |
| 비율/구성 | **pie** / **donut** | 항목 ≤ 8 권장 |
| 두 수치 상관 | **scatter** | text 컬럼으로 레이블 표시 |
| 두 범주 × 수치 교차 | **heatmap** | 교차표 형태 |
| 계층 구조 + 크기 | **treemap** | 상·하위 관계 필수 아님 |
| 흐름 (A→B + 볼륨) | **sankey** | source/target/value 3컬럼 |
| 단계별 전환/이탈 | **funnel** | 순서 있는 퍼널 |

---

## Config JSON mapping 키

### bar / grouped bar

```json
{
  "type": "bar",
  "title": "월별 매출",
  "data_csv": "sales.csv",
  "mapping": { "x": "월", "y": "매출액" }
}
```

그룹 비교 (color 추가 시 자동 grouped):
```json
{ "mapping": { "x": "월", "y": "매출액", "color": "채널" } }
```

### stacked_bar

color 컬럼 필수:
```json
{
  "type": "stacked_bar",
  "mapping": { "x": "분기", "y": "매출액", "color": "제품군" }
}
```

### line

`y`에 리스트로 다중 라인:
```json
{
  "type": "line",
  "mapping": { "x": "날짜", "y": ["매출", "비용", "이익"] }
}
```

### pie / donut

```json
{
  "type": "donut",
  "mapping": { "labels": "채널", "values": "방문수" }
}
```

### scatter

```json
{
  "type": "scatter",
  "mapping": { "x": "광고비", "y": "전환수", "text": "캠페인명" }
}
```
`text` 생략 시 x값이 호버 레이블로 사용됨.

### heatmap

교차표 형태 데이터 (행: y, 열: x, 값: value):
```json
{
  "type": "heatmap",
  "mapping": { "x": "요일", "y": "시간대", "value": "방문수" }
}
```

### treemap

`parent` 생략 시 단일 레벨 트리맵:
```json
{
  "type": "treemap",
  "mapping": { "labels": "카테고리", "values": "매출액", "parent": "대분류" }
}
```

### sankey

source → target 흐름 데이터:
```json
{
  "type": "sankey",
  "mapping": { "source": "유입경로", "target": "페이지", "value": "세션수" }
}
```

### funnel

순서가 있는 퍼널 데이터 (위에서 아래로 줄어드는 구조):
```json
{
  "type": "funnel",
  "mapping": { "labels": "단계", "values": "사용자수" }
}
```

---

## data_rows 인라인 (CSV 파일 없을 때)

클립보드 데이터나 소량 데이터는 `data_rows`로 직접 전달:
```json
{
  "type": "bar",
  "title": "채널별 방문",
  "data_rows": [
    {"채널": "검색", "방문": "4500"},
    {"채널": "직접", "방문": "2100"},
    {"채널": "SNS", "방문": "1800"}
  ],
  "mapping": { "x": "채널", "y": "방문" }
}
```

---

## 복합 시각화

동일 데이터로 여러 차트 생성 시 config를 여러 개 작성해 순차 실행:
```bash
python3 scripts/generate_chart.py --config overview_config.json
python3 scripts/generate_chart.py --config detail_config.json
```
