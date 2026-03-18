# 시각화 유형 가이드

## 유형 선택 기준 (데이터 특성 → 차트)

| 데이터 특성 | 추천 유형 | 비고 |
|-------------|-----------|------|
| 범주별 수치 비교 | **bar** | 항목 수 ≤ 20일 때 |
| 범주별 수치 + 그룹 구분 | **stacked_bar** | mapping에 `color` 컬럼 추가 |
| 시계열 추이 | **line** | `y`에 복수 컬럼 가능 |
| 비율/구성 | **pie** / **donut** | 항목 수 ≤ 8일 때 가독성 좋음 |
| 두 수치 간 상관 | **scatter** | 분포 패턴 확인용 |
| 두 범주 × 수치 | **heatmap** | 교차표 형태 데이터 |
| 계층 구조 + 크기 | **treemap** | 상위/하위 관계가 있을 때 |
| 흐름 (출발→도착 + 볼륨) | **sankey** | 노드 간 이동량 시각화 |
| 단계별 전환/이탈 | **funnel** | 순서가 명확한 퍼널 데이터 |

## Config JSON mapping 키

### bar / stacked_bar

```json
{
  "type": "bar",
  "mapping": { "x": "범주 컬럼", "y": "수치 컬럼", "color": "그룹 컬럼 (선택)" }
}
```

### line

```json
{
  "type": "line",
  "mapping": { "x": "시간/범주 컬럼", "y": "수치 컬럼" }
}
```
`y`에 리스트를 주면 다중 라인: `"y": ["매출", "비용"]`

### pie / donut

```json
{
  "type": "pie",
  "mapping": { "labels": "범주 컬럼", "values": "수치 컬럼" }
}
```

### scatter

```json
{
  "type": "scatter",
  "mapping": { "x": "수치 컬럼A", "y": "수치 컬럼B", "text": "라벨 컬럼 (선택)" }
}
```

### heatmap

```json
{
  "type": "heatmap",
  "mapping": { "x": "범주 컬럼A", "y": "범주 컬럼B", "value": "수치 컬럼" }
}
```

### treemap

```json
{
  "type": "treemap",
  "mapping": { "labels": "항목 컬럼", "values": "크기 컬럼", "parent": "상위항목 컬럼 (선택)" }
}
```

### sankey

```json
{
  "type": "sankey",
  "mapping": { "source": "출발 컬럼", "target": "도착 컬럼", "value": "볼륨 컬럼" }
}
```

### funnel

```json
{
  "type": "funnel",
  "mapping": { "labels": "단계 컬럼", "values": "수치 컬럼" }
}
```

## 복합 시각화

하나의 데이터로 여러 차트를 생성할 수 있다. config JSON을 여러 개 작성하여 순차 실행한다.
