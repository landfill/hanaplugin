#!/usr/bin/env python3
"""
generate_funnel.py
CSV 트래픽 리포트에서 퍼널(Funnel) 또는 Stacked bar HTML을 생성한다.
LLM 없이 반복 실행 가능한 결정적(deterministic) 변환기.

Usage:
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --list
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 패키지
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 항공(해외) --type stacked
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 패키지 --output docs/패키지_funnel.html
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


_EXAMPLES_DIR = Path(__file__).parent
_SCRIPTS_DIR = _EXAMPLES_DIR.parent / "scripts"


def _load_json(path: Path) -> dict:
    if not path.exists():
        print(f"오류: {path} 파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


CATEGORY_FLOWS: dict[str, list[str]] = _load_json(_EXAMPLES_DIR / "hanatour_categories.json")
_BRAND = _load_json(_SCRIPTS_DIR / "brand_colors.json")

PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.32.0.min.js"

FUNNEL_COLORS = _BRAND["funnel_colors"]
WEB_COLOR = _BRAND["web_color"]
PC_COLOR = _BRAND["pc_color"]
T = _BRAND["theme"]


def parse_number(val: str) -> int | None:
    val = val.strip().replace(",", "")
    if not val:
        return None
    try:
        return int(float(val))
    except ValueError:
        return None


def parse_rate(val: str) -> str:
    val = val.strip()
    if not val:
        return "—"
    if "↓" in val:
        sign = "-"
    elif "↑" in val:
        sign = "+"
    else:
        sign = ""
    num = re.sub(r"[^0-9.]", "", val)
    return f"{sign}{num}%" if num else val


def load_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def list_categories(rows: list[dict]) -> list[str]:
    seen = []
    for row in rows:
        cat = row.get("구분1", "").strip()
        if cat and cat not in seen:
            seen.append(cat)
    return seen


def extract_nodes(rows: list[dict], category: str, steps: list[str]) -> list[dict]:
    lookup: dict[str, dict] = {}
    for row in rows:
        cat = row.get("구분1", "").strip()
        sub = row.get("구분2", "").strip()
        if cat == category and sub in steps:
            lookup[sub] = row

    nodes = []
    for step in steps:
        if step not in lookup:
            print(f"  [경고] '{category} / {step}' 행을 CSV에서 찾을 수 없습니다.", file=sys.stderr)
            continue
        r = lookup[step]
        nodes.append({
            "label": step,
            "uv": parse_number(r.get("합계_UV", "")) or 0,
            "prevUv": parse_number(r.get("합계_전주UV", "")) or 0,
            "rate": parse_rate(r.get("합계_증감률", "")),
            "webUv": parse_number(r.get("Web_UV", "")) or 0,
            "webPrev": parse_number(r.get("Web_전주UV", "")) or 0,
            "webRate": parse_rate(r.get("Web_증감률", "")),
            "webShare": r.get("Web_전체대비", "").strip() or "—",
            "pcUv": parse_number(r.get("PC_UV", "")) or 0,
            "pcPrev": parse_number(r.get("PC_전주UV", "")) or 0,
            "pcRate": parse_rate(r.get("PC_증감률", "")),
            "pcShare": r.get("PC_전체대비", "").strip() or "—",
            "conv": r.get("합계_전환율", "").strip() or None,
            "webConv": r.get("Web_전환율", "").strip() or None,
            "pcConv": r.get("PC_전환율", "").strip() or None,
        })
    return nodes


def render_funnel_html(category: str, nodes: list[dict]) -> str:
    """단계별 전환율 퍼널 차트"""
    labels = [n["label"] for n in nodes]
    uvs = [n["uv"] for n in nodes]
    base = uvs[0] if uvs[0] > 0 else 1
    conv_rates = [f"{v / base * 100:.1f}%" for v in uvs]

    # 단계 간 전환율
    step_rates = []
    for i in range(len(nodes) - 1):
        prev = nodes[i]["uv"]
        cur = nodes[i + 1]["uv"]
        step_rates.append(f"{cur / prev * 100:.1f}%" if prev > 0 else "—")

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    labels_json = json.dumps(labels, ensure_ascii=False)
    uvs_json = json.dumps(uvs)
    conv_json = json.dumps(conv_rates)
    step_json = json.dumps(step_rates)
    colors_json = json.dumps(FUNNEL_COLORS[: len(nodes)])
    subtitle = " → ".join(labels)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{category} 퍼널 — Funnel</title>
  <script src="{PLOTLY_CDN}"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
      background: {T['bg']}; color: {T['text']};
      min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; padding: 32px 16px;
    }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; }}
    .subtitle {{ font-size: 0.82rem; color: {T['text_muted']}; margin-bottom: 24px; }}
    #chart {{ width: 100%; max-width: 760px; }}
    .card-overlay {{
      display: none; position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background: {T['surface']}; border: 1px solid {T['border']};
      border-radius: 12px; padding: 20px 24px; min-width: 280px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5); z-index: 100;
    }}
    .card-overlay h2 {{
      font-size: 1rem; font-weight: 700; margin-bottom: 14px;
      color: {T['card_title']}; border-bottom: 1px solid {T['border']}; padding-bottom: 10px;
    }}
    .card-row {{
      display: flex; justify-content: space-between;
      margin-bottom: 8px; font-size: 0.85rem;
    }}
    .card-label {{ color: {T['text_muted']}; }}
    .card-value {{ font-weight: 600; }}
    .up {{ color: {T['up']}; }} .down {{ color: {T['down']}; }}
    .card-close {{
      position: absolute; top: 10px; right: 14px;
      cursor: pointer; font-size: 1.1rem; color: {T['text_muted']};
      background: none; border: none;
    }}
    .step-table {{
      margin-top: 16px; width: 100%; max-width: 760px;
      border-collapse: collapse; font-size: 0.82rem;
    }}
    .step-table th, .step-table td {{
      padding: 6px 12px; border-bottom: 1px solid {T['grid']}; text-align: right;
    }}
    .step-table th {{ color: {T['text_muted']}; text-align: center; }}
    .step-table td:first-child {{ text-align: left; }}
  </style>
</head>
<body>
<h1>{category} 퍼널</h1>
<p class="subtitle">{subtitle} / 막대 클릭 시 상세 지표</p>
<div id="chart"></div>

<table class="step-table">
  <thead><tr><th>단계</th><th>UV</th><th>전주 대비</th><th>진입 전환율</th><th>단계간 전환율</th></tr></thead>
  <tbody id="stepBody"></tbody>
</table>

<div class="card-overlay" id="detailCard">
  <button class="card-close" onclick="closeCard()">✕</button>
  <h2 id="cardTitle"></h2>
  <div id="cardBody"></div>
</div>

<script>
const nodeData = {nodes_json};
const labels = {labels_json};
const uvs = {uvs_json};
const convRates = {conv_json};
const stepRates = {step_json};

// 테이블 생성
const tbody = document.getElementById('stepBody');
nodeData.forEach((d, i) => {{
  const rc = d.rate.startsWith('+') ? 'up' : (d.rate.startsWith('-') ? 'down' : '');
  const sr = i > 0 ? stepRates[i-1] : '—';
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>${{d.label}}</td>
    <td>${{d.uv.toLocaleString()}}</td>
    <td class="${{rc}}">${{d.rate}}</td>
    <td>${{convRates[i]}}</td>
    <td>${{sr}}</td>
  `;
  tbody.appendChild(tr);
}});

const trace = {{
  type: 'funnel',
  y: labels,
  x: uvs,
  textinfo: 'value+percent initial',
  textposition: 'inside',
  marker: {{ color: {colors_json} }},
  connector: {{ line: {{ color: '{T['connector']}', width: 2 }} }},
  hovertemplate: '%{{y}}<br>UV: %{{x:,}}<br>누적 전환율: %{{customdata}}<extra></extra>',
  customdata: convRates,
  orientation: 'h'
}};
const layout = {{
  paper_bgcolor: '{T['bg']}', plot_bgcolor: '{T['bg']}',
  font: {{ family: 'Noto Sans KR, Apple SD Gothic Neo, sans-serif', color: '{T['text']}', size: 13 }},
  height: 360, margin: {{ t: 20, b: 20, l: 10, r: 10 }},
  funnelmode: 'stack'
}};
Plotly.newPlot('chart', [trace], layout, {{ responsive: true, displayModeBar: false }});

document.getElementById('chart').on('plotly_click', function(data) {{
  const idx = data.points[0].pointNumber;
  if (idx !== undefined && idx < nodeData.length) showCard(nodeData[idx]);
}});

function rateClass(r) {{ return r.startsWith('+') ? 'up' : (r.startsWith('-') ? 'down' : ''); }}
function row(label, val, cls='') {{
  return `<div class="card-row"><span class="card-label">${{label}}</span><span class="card-value ${{cls}}">${{val}}</span></div>`;
}}
function showCard(d) {{
  document.getElementById('cardTitle').textContent = d.label;
  let html = row('합계 UV', d.uv.toLocaleString())
    + row('전주 UV', d.prevUv.toLocaleString())
    + row('증감률', d.rate, rateClass(d.rate))
    + row('Web UV', `${{d.webUv.toLocaleString()}} (${{d.webShare}})`)
    + row('Web 증감률', d.webRate, rateClass(d.webRate))
    + row('PC UV', `${{d.pcUv.toLocaleString()}} (${{d.pcShare}})`)
    + row('PC 증감률', d.pcRate, rateClass(d.pcRate));
  if (d.conv) html += row('전환율', d.conv, 'up');
  document.getElementById('cardBody').innerHTML = html;
  document.getElementById('detailCard').style.display = 'block';
}}
function closeCard() {{ document.getElementById('detailCard').style.display = 'none'; }}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeCard(); }});
</script>
</body>
</html>"""


def render_stacked_html(category: str, nodes: list[dict]) -> str:
    """Web / PC 채널 Stacked bar 차트"""
    labels = [n["label"] for n in nodes]
    web_uvs = [n["webUv"] for n in nodes]
    pc_uvs = [n["pcUv"] for n in nodes]
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    labels_json = json.dumps(labels, ensure_ascii=False)
    web_json = json.dumps(web_uvs)
    pc_json = json.dumps(pc_uvs)
    subtitle = " | ".join(labels)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{category} Web·PC 채널 — Stacked Bar</title>
  <script src="{PLOTLY_CDN}"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
      background: {T['bg']}; color: {T['text']};
      min-height: 100vh; display: flex; flex-direction: column;
      align-items: center; padding: 32px 16px;
    }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; }}
    .subtitle {{ font-size: 0.82rem; color: {T['text_muted']}; margin-bottom: 24px; }}
    #chart {{ width: 100%; max-width: 900px; }}
    .card-overlay {{
      display: none; position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background: {T['surface']}; border: 1px solid {T['border']};
      border-radius: 12px; padding: 20px 24px; min-width: 280px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5); z-index: 100;
    }}
    .card-overlay h2 {{
      font-size: 1rem; font-weight: 700; margin-bottom: 14px;
      color: {T['card_title']}; border-bottom: 1px solid {T['border']}; padding-bottom: 10px;
    }}
    .card-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.85rem; }}
    .card-label {{ color: {T['text_muted']}; }}
    .card-value {{ font-weight: 600; }}
    .up {{ color: {T['up']}; }} .down {{ color: {T['down']}; }}
    .card-close {{
      position: absolute; top: 10px; right: 14px;
      cursor: pointer; font-size: 1.1rem; color: {T['text_muted']};
      background: none; border: none;
    }}
  </style>
</head>
<body>
<h1>{category} Web · PC 채널</h1>
<p class="subtitle">{subtitle} / 막대 클릭 시 상세 지표</p>
<div id="chart"></div>

<div class="card-overlay" id="detailCard">
  <button class="card-close" onclick="closeCard()">✕</button>
  <h2 id="cardTitle"></h2>
  <div id="cardBody"></div>
</div>

<script>
const nodeData = {nodes_json};
const traceWeb = {{
  name: 'Web',
  type: 'bar', x: {labels_json}, y: {web_json},
  marker: {{ color: '{WEB_COLOR}' }},
  hovertemplate: 'Web: %{{y:,}}<extra></extra>'
}};
const tracePC = {{
  name: 'PC',
  type: 'bar', x: {labels_json}, y: {pc_json},
  marker: {{ color: '{PC_COLOR}' }},
  hovertemplate: 'PC: %{{y:,}}<extra></extra>'
}};
const layout = {{
  barmode: 'stack',
  paper_bgcolor: '{T['bg']}', plot_bgcolor: '{T['bg']}',
  font: {{ family: 'Noto Sans KR, Apple SD Gothic Neo, sans-serif', color: '{T['text']}', size: 13 }},
  height: 400, margin: {{ t: 20, b: 60, l: 60, r: 10 }},
  legend: {{ orientation: 'h', y: -0.2 }},
  xaxis: {{ tickfont: {{ color: '{T['text']}' }}, gridcolor: '{T['grid']}' }},
  yaxis: {{ tickfont: {{ color: '{T['text']}' }}, gridcolor: '{T['grid']}' }}
}};
Plotly.newPlot('chart', [traceWeb, tracePC], layout, {{ responsive: true, displayModeBar: false }});

document.getElementById('chart').on('plotly_click', function(data) {{
  const idx = data.points[0].pointNumber;
  if (idx !== undefined && idx < nodeData.length) showCard(nodeData[idx]);
}});

function rateClass(r) {{ return r.startsWith('+') ? 'up' : (r.startsWith('-') ? 'down' : ''); }}
function row(label, val, cls='') {{
  return `<div class="card-row"><span class="card-label">${{label}}</span><span class="card-value ${{cls}}">${{val}}</span></div>`;
}}
function showCard(d) {{
  document.getElementById('cardTitle').textContent = d.label;
  const total = d.webUv + d.pcUv;
  const webPct = total > 0 ? (d.webUv / total * 100).toFixed(1) + '%' : '—';
  const pcPct = total > 0 ? (d.pcUv / total * 100).toFixed(1) + '%' : '—';
  let html = row('합계 UV', d.uv.toLocaleString())
    + row('증감률', d.rate, rateClass(d.rate))
    + row('Web UV', `${{d.webUv.toLocaleString()}} (${{webPct}})`)
    + row('Web 증감률', d.webRate, rateClass(d.webRate))
    + row('PC UV', `${{d.pcUv.toLocaleString()}} (${{pcPct}})`)
    + row('PC 증감률', d.pcRate, rateClass(d.pcRate));
  document.getElementById('cardBody').innerHTML = html;
  document.getElementById('detailCard').style.display = 'block';
}}
function closeCard() {{ document.getElementById('detailCard').style.display = 'none'; }}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeCard(); }});
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description="CSV 트래픽 리포트 → 퍼널/Stacked bar HTML 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --list
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 패키지
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 항공(해외) --type stacked
  python3 scripts/generate_funnel.py --csv docs/uv_report.csv --category 패키지 --output docs/패키지_funnel.html
        """,
    )
    parser.add_argument("--csv", required=True, help="입력 CSV 경로")
    parser.add_argument("--category", help="시각화할 구분1 카테고리")
    parser.add_argument("--type", choices=["funnel", "stacked"], default="funnel",
                        help="차트 유형: funnel(기본) 또는 stacked(Web/PC 채널)")
    parser.add_argument("--output", help="출력 HTML 경로 (기본: docs/<category>_<type>.html)")
    parser.add_argument("--list", action="store_true", help="CSV 내 카테고리 목록 출력 후 종료")

    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"오류: CSV 파일을 찾을 수 없습니다 — {csv_path}", file=sys.stderr)
        sys.exit(1)

    rows = load_csv(csv_path)

    if args.list:
        cats = list_categories(rows)
        print("CSV 내 구분1 카테고리:")
        for c in cats:
            flow = CATEGORY_FLOWS.get(c)
            status = f"→  {' → '.join(flow)}  [흐름 정의 있음]" if flow else "[흐름 미정의]"
            print(f"  {c}  {status}")
        sys.exit(0)

    if not args.category:
        parser.error("--category 또는 --list 중 하나를 지정하세요.")

    category = args.category
    steps = CATEGORY_FLOWS.get(category)
    if not steps:
        print(f"오류: '{category}' 의 흐름 정의가 없습니다. CATEGORY_FLOWS에 추가하세요.", file=sys.stderr)
        sys.exit(1)

    nodes = extract_nodes(rows, category, steps)
    if not nodes:
        print(f"오류: '{category}' 데이터를 CSV에서 추출할 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    if args.type == "stacked":
        html = render_stacked_html(category, nodes)
        default_suffix = "stacked"
    else:
        html = render_funnel_html(category, nodes)
        default_suffix = "funnel"

    if args.output:
        out_path = Path(args.output)
    else:
        safe_name = re.sub(r"[^\w]", "_", category, flags=re.UNICODE)
        out_path = csv_path.parent / f"{safe_name}_{default_suffix}.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"생성 완료: {out_path}")
    print(f"  카테고리: {category}  /  유형: {args.type}")
    print(f"  단계: {' → '.join(n['label'] for n in nodes)}")


if __name__ == "__main__":
    main()
