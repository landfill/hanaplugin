#!/usr/bin/env python3
"""
generate_chart.py
범용 차트 생성기. JSON config를 입력받아 Plotly.js 기반 단일 HTML을 출력한다.

지원 차트 유형:
  bar, stacked_bar, line, pie, donut, scatter, heatmap, treemap, sankey, funnel

Usage:
  python3 generate_chart.py --config chart_config.json
  python3 generate_chart.py --config chart_config.json --output docs/result.html
  echo '{"type":"bar",...}' | python3 generate_chart.py --config -

Config JSON 구조 (최소):
  {
    "type": "bar",
    "title": "차트 제목",
    "data_csv": "docs/data.csv",
    "mapping": { "x": "컬럼A", "y": "컬럼B" }
  }
"""

import argparse
import csv
import json
import sys
from pathlib import Path


_SCRIPTS_DIR = Path(__file__).parent
PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.32.0.min.js"


def _load_brand_colors() -> dict:
    """brand_colors.json이 있으면 로드, 없으면 기본값."""
    brand_path = _SCRIPTS_DIR / "brand_colors.json"
    if brand_path.exists():
        with open(brand_path, encoding="utf-8") as f:
            return json.load(f)
    return {
        "node_colors": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
                         "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"],
        "funnel_colors": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"],
        "link_colors": ["rgba(99,110,250,0.35)", "rgba(239,85,59,0.35)",
                         "rgba(0,204,150,0.35)", "rgba(171,99,250,0.35)"],
        "web_color": "#636EFA",
        "pc_color": "#00CC96",
        "theme": {
            "bg": "#0f1117", "surface": "#1e2130", "border": "#3a3d5c",
            "text": "#e8eaf6", "text_muted": "#9e9eb8", "card_title": "#a5b4fc",
            "up": "#6ee7b7", "down": "#f87171", "meta": "#555870",
            "grid": "#2a2d45", "connector": "#3a3d5c"
        }
    }


_BRAND = _load_brand_colors()
T = _BRAND["theme"]
COLORS = _BRAND.get("node_colors", _BRAND.get("funnel_colors", []))


def load_csv_data(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def extract_col(rows: list[dict], col: str) -> list:
    return [r.get(col, "").strip() for r in rows]


def to_numeric(values: list[str]) -> list[float]:
    result = []
    for v in values:
        v = v.replace(",", "").replace("%", "").replace("↑", "").replace("↓", "")
        try:
            result.append(float(v))
        except ValueError:
            result.append(0.0)
    return result


# ── 차트 생성 함수들 ────────────────────────────────────────

def _html_shell(title: str, body: str, extra_style: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <script src="{PLOTLY_CDN}"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
      background: {T['bg']}; color: {T['text']};
      min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; padding: 32px 16px;
    }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; letter-spacing: -0.5px; }}
    .subtitle {{ font-size: 0.82rem; color: {T['text_muted']}; margin-bottom: 24px; }}
    #chart {{ width: 100%; max-width: 960px; }}
    {extra_style}
  </style>
</head>
<body>
{body}
</body>
</html>"""


def _plotly_layout(title: str = "", height: int = 480) -> dict:
    return {
        "paper_bgcolor": T["bg"],
        "plot_bgcolor": T["bg"],
        "font": {"family": "Noto Sans KR, Apple SD Gothic Neo, sans-serif", "color": T["text"], "size": 13},
        "height": height,
        "margin": {"t": 40, "b": 60, "l": 60, "r": 20},
        "title": {"text": title, "font": {"size": 16}},
        "xaxis": {"tickfont": {"color": T["text"]}, "gridcolor": T["grid"]},
        "yaxis": {"tickfont": {"color": T["text"]}, "gridcolor": T["grid"]},
        "legend": {"orientation": "h", "y": -0.15},
    }


def gen_bar(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    x = extract_col(rows, m["x"])
    y = to_numeric(extract_col(rows, m["y"]))
    color_col = m.get("color")

    if color_col:
        # grouped bar
        groups = {}
        for r in rows:
            g = r.get(color_col, "").strip()
            if g not in groups:
                groups[g] = {"x": [], "y": []}
            groups[g]["x"].append(r.get(m["x"], "").strip())
            groups[g]["y"].append(to_numeric([r.get(m["y"], "")])[0])

        traces = []
        for i, (g, data) in enumerate(groups.items()):
            traces.append({
                "type": "bar", "name": g,
                "x": data["x"], "y": data["y"],
                "marker": {"color": COLORS[i % len(COLORS)]}
            })
    else:
        traces = [{"type": "bar", "x": x, "y": y, "marker": {"color": COLORS[:len(x)]}}]

    layout = _plotly_layout(config.get("title", ""))
    if config["type"] == "stacked_bar":
        layout["barmode"] = "stack"

    traces_json = json.dumps(traces, ensure_ascii=False)
    layout_json = json.dumps(layout, ensure_ascii=False)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', {traces_json}, {layout_json}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Bar Chart"), body)


def gen_line(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    x = extract_col(rows, m["x"])
    y_cols = m["y"] if isinstance(m["y"], list) else [m["y"]]

    traces = []
    for i, col in enumerate(y_cols):
        traces.append({
            "type": "scatter", "mode": "lines+markers",
            "name": col, "x": x, "y": to_numeric(extract_col(rows, col)),
            "line": {"color": COLORS[i % len(COLORS)]}
        })

    layout = _plotly_layout(config.get("title", ""))
    traces_json = json.dumps(traces, ensure_ascii=False)
    layout_json = json.dumps(layout, ensure_ascii=False)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', {traces_json}, {layout_json}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Line Chart"), body)


def gen_pie(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    labels = extract_col(rows, m["labels"])
    values = to_numeric(extract_col(rows, m["values"]))
    hole = 0.4 if config["type"] == "donut" else 0

    trace = {
        "type": "pie", "labels": labels, "values": values,
        "hole": hole, "marker": {"colors": COLORS[:len(labels)]},
        "textinfo": "label+percent", "textposition": "inside"
    }
    layout = _plotly_layout(config.get("title", ""), height=500)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Pie Chart"), body)


def gen_scatter(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    x = to_numeric(extract_col(rows, m["x"]))
    y = to_numeric(extract_col(rows, m["y"]))
    text = extract_col(rows, m.get("text", m["x"]))

    trace = {
        "type": "scatter", "mode": "markers",
        "x": x, "y": y, "text": text,
        "marker": {"color": COLORS[0], "size": 10, "opacity": 0.7},
        "hovertemplate": "%{text}<br>x: %{x}<br>y: %{y}<extra></extra>"
    }
    layout = _plotly_layout(config.get("title", ""))
    layout["xaxis"]["title"] = m["x"]
    layout["yaxis"]["title"] = m["y"]

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Scatter Plot"), body)


def gen_heatmap(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    x_labels = sorted(set(extract_col(rows, m["x"])))
    y_labels = sorted(set(extract_col(rows, m["y"])))
    z = [[0.0] * len(x_labels) for _ in y_labels]

    for r in rows:
        xv = r.get(m["x"], "").strip()
        yv = r.get(m["y"], "").strip()
        val = to_numeric([r.get(m["value"], "0")])[0]
        if xv in x_labels and yv in y_labels:
            z[y_labels.index(yv)][x_labels.index(xv)] = val

    trace = {
        "type": "heatmap", "x": x_labels, "y": y_labels, "z": z,
        "colorscale": [[0, T["bg"]], [1, COLORS[0]]],
        "hovertemplate": "%{x} / %{y}: %{z}<extra></extra>"
    }
    layout = _plotly_layout(config.get("title", ""), height=500)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Heatmap"), body)


def gen_treemap(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    parents_col = m.get("parent", "")
    labels = extract_col(rows, m["labels"])
    values = to_numeric(extract_col(rows, m["values"]))
    parents = extract_col(rows, parents_col) if parents_col else [""] * len(labels)

    trace = {
        "type": "treemap",
        "labels": labels, "parents": parents, "values": values,
        "marker": {"colors": COLORS[:len(labels)]},
        "textinfo": "label+value+percent root"
    }
    layout = _plotly_layout(config.get("title", ""), height=550)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Treemap"), body)


def gen_sankey(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    sources_str = extract_col(rows, m["source"])
    targets_str = extract_col(rows, m["target"])
    values = to_numeric(extract_col(rows, m["value"]))

    all_labels = list(dict.fromkeys(sources_str + targets_str))
    sources = [all_labels.index(s) for s in sources_str]
    targets = [all_labels.index(t) for t in targets_str]

    link_colors = _BRAND.get("link_colors", [])
    lc = [link_colors[i % len(link_colors)] if link_colors else "rgba(128,128,128,0.3)" for i in range(len(sources))]

    trace = {
        "type": "sankey", "orientation": "h",
        "node": {
            "pad": 24, "thickness": 28,
            "line": {"color": T["surface"], "width": 1.5},
            "label": all_labels,
            "color": [COLORS[i % len(COLORS)] for i in range(len(all_labels))]
        },
        "link": {"source": sources, "target": targets, "value": values, "color": lc}
    }
    layout = _plotly_layout(config.get("title", ""), height=450)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Sankey"), body)


def gen_funnel(config: dict, rows: list[dict]) -> str:
    m = config["mapping"]
    labels = extract_col(rows, m["labels"])
    values = to_numeric(extract_col(rows, m["values"]))
    colors = _BRAND.get("funnel_colors", COLORS)

    trace = {
        "type": "funnel", "y": labels, "x": values,
        "textinfo": "value+percent initial", "textposition": "inside",
        "marker": {"color": colors[:len(labels)]},
        "connector": {"line": {"color": T["connector"], "width": 2}},
        "orientation": "h"
    }
    layout = _plotly_layout(config.get("title", ""), height=400)
    layout["funnelmode"] = "stack"

    body = f"""<div id="chart"></div>
<script>
Plotly.newPlot('chart', [{json.dumps(trace, ensure_ascii=False)}],
  {json.dumps(layout, ensure_ascii=False)}, {{responsive:true, displayModeBar:false}});
</script>"""
    return _html_shell(config.get("title", "Funnel"), body)


# ── 디스패처 ────────────────────────────────────────────────

GENERATORS = {
    "bar": gen_bar,
    "stacked_bar": gen_bar,
    "line": gen_line,
    "pie": gen_pie,
    "donut": gen_pie,
    "scatter": gen_scatter,
    "heatmap": gen_heatmap,
    "treemap": gen_treemap,
    "sankey": gen_sankey,
    "funnel": gen_funnel,
}


def main():
    parser = argparse.ArgumentParser(
        description="범용 차트 생성기 — JSON config → Plotly HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
지원 유형: bar, stacked_bar, line, pie, donut, scatter, heatmap, treemap, sankey, funnel

Config 예시 (bar):
  {"type": "bar", "title": "매출", "data_csv": "data.csv", "mapping": {"x": "월", "y": "매출액"}}

Config 예시 (sankey):
  {"type": "sankey", "title": "흐름", "data_csv": "flow.csv", "mapping": {"source": "출발", "target": "도착", "value": "건수"}}
        """,
    )
    parser.add_argument("--config", help="JSON config 파일 경로 (또는 - 로 stdin)")
    parser.add_argument("--output", help="출력 HTML 경로")
    parser.add_argument("--list-types", action="store_true", help="지원 차트 유형 출력")

    args = parser.parse_args()

    if args.list_types:
        print("지원 차트 유형:")
        for t in GENERATORS:
            print(f"  {t}")
        sys.exit(0)

    if not args.config:
        parser.error("--config 또는 --list-types 중 하나를 지정하세요.")

    # config 로드
    if args.config == "-":
        config = json.load(sys.stdin)
    else:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"오류: config 파일을 찾을 수 없습니다 — {config_path}", file=sys.stderr)
            sys.exit(1)
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

    chart_type = config.get("type", "")
    if chart_type not in GENERATORS:
        print(f"오류: 지원하지 않는 차트 유형 — '{chart_type}'", file=sys.stderr)
        print(f"  지원 유형: {', '.join(GENERATORS.keys())}", file=sys.stderr)
        sys.exit(1)

    data_csv = config.get("data_csv", "")
    if not data_csv or not Path(data_csv).exists():
        print(f"오류: data_csv 파일을 찾을 수 없습니다 — '{data_csv}'", file=sys.stderr)
        sys.exit(1)

    rows = load_csv_data(data_csv)
    if not rows:
        print("오류: CSV 데이터가 비어 있습니다.", file=sys.stderr)
        sys.exit(1)

    html = GENERATORS[chart_type](config, rows)

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(data_csv).parent / f"{Path(data_csv).stem}_{chart_type}.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"생성 완료: {out_path}")
    print(f"  유형: {chart_type}  /  데이터: {len(rows)}행")


if __name__ == "__main__":
    main()
