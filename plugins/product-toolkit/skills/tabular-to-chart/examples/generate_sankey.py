#!/usr/bin/env python3
"""
generate_sankey.py
CSV 트래픽 리포트에서 Sankey HTML을 생성한다.
LLM 없이 반복 실행 가능한 결정적(deterministic) 변환기.

Usage:
  python scripts/generate_sankey.py --csv docs/uv_report.csv --category 패키지
  python scripts/generate_sankey.py --csv docs/uv_report.csv --category 항공(해외) --output docs/항공_sankey.html
  python scripts/generate_sankey.py --csv docs/uv_report.csv --list
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

NODE_COLORS = _BRAND["node_colors"]
LINK_COLORS = _BRAND["link_colors"]
WEB_COLOR = _BRAND["web_color"]
PC_COLOR = _BRAND["pc_color"]
T = _BRAND["theme"]


def parse_number(val: str) -> int | None:
    """'1,234' → 1234, 빈 문자열 → None"""
    val = val.strip().replace(",", "")
    if not val:
        return None
    try:
        return int(float(val))
    except ValueError:
        return None


def parse_rate(val: str) -> str:
    """'6.2%↓' → '-6.2%', '3.6%↑' → '+3.6%'"""
    val = val.strip()
    if not val:
        return "—"
    sign = "-" if "↓" in val else "+"
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
    """category + steps 조합으로 노드 데이터 추출"""
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
        uv = parse_number(r.get("합계_UV", ""))
        prev = parse_number(r.get("합계_전주UV", ""))
        rate = parse_rate(r.get("합계_증감률", ""))
        web_uv = parse_number(r.get("Web_UV", ""))
        web_prev = parse_number(r.get("Web_전주UV", ""))
        web_rate = parse_rate(r.get("Web_증감률", ""))
        web_share = r.get("Web_전체대비", "").strip() or "—"
        pc_uv = parse_number(r.get("PC_UV", ""))
        pc_prev = parse_number(r.get("PC_전주UV", ""))
        pc_rate = parse_rate(r.get("PC_증감률", ""))
        pc_share = r.get("PC_전체대비", "").strip() or "—"
        conv = r.get("합계_전환율", "").strip() or None
        web_conv = r.get("Web_전환율", "").strip() or None
        pc_conv = r.get("PC_전환율", "").strip() or None

        nodes.append({
            "label": step,
            "uv": uv or 0,
            "prevUv": prev or 0,
            "rate": rate,
            "webUv": web_uv or 0,
            "webPrev": web_prev or 0,
            "webRate": web_rate,
            "webShare": web_share,
            "pcUv": pc_uv or 0,
            "pcPrev": pc_prev or 0,
            "pcRate": pc_rate,
            "pcShare": pc_share,
            "conv": conv,
            "webConv": web_conv,
            "pcConv": pc_conv,
        })
    return nodes


def build_links(nodes: list[dict]) -> tuple[list[int], list[int], list[int], list[str]]:
    sources, targets, values, conv_labels = [], [], [], []
    for i in range(len(nodes) - 1):
        sources.append(i)
        targets.append(i + 1)
        values.append(nodes[i + 1]["uv"])  # 다음 단계 UV = 링크 볼륨
        if nodes[i]["uv"] > 0:
            rate = nodes[i + 1]["uv"] / nodes[i]["uv"] * 100
            conv_labels.append(f"{rate:.1f}%")
        else:
            conv_labels.append("—")
    return sources, targets, values, conv_labels


def render_html(category: str, nodes: list[dict]) -> str:
    sources, targets, values, conv_labels = build_links(nodes)

    node_colors = NODE_COLORS[: len(nodes)]
    link_colors = LINK_COLORS[: len(nodes) - 1]

    node_labels = [
        f"{n['label']}<br>{n['uv']:,} UV" for n in nodes
    ]

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    sources_json = json.dumps(sources)
    targets_json = json.dumps(targets)
    values_json = json.dumps(values)
    conv_json = json.dumps(conv_labels)
    node_labels_json = json.dumps(node_labels, ensure_ascii=False)
    node_colors_json = json.dumps(node_colors)
    link_colors_json = json.dumps(link_colors)

    subtitle_steps = " → ".join(n["label"] for n in nodes)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{category} 트래픽 흐름 — Sankey</title>
  <script src="{PLOTLY_CDN}"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
      background: {T['bg']};
      color: {T['text']};
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 32px 16px;
    }}
    h1 {{ font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; letter-spacing: -0.5px; }}
    .subtitle {{ font-size: 0.82rem; color: {T['text_muted']}; margin-bottom: 24px; }}
    #chart {{ width: 100%; max-width: 960px; }}
    .card-overlay {{
      display: none;
      position: fixed; top: 50%; left: 50%;
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
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 8px; font-size: 0.85rem;
    }}
    .card-label {{ color: {T['text_muted']}; }}
    .card-value {{ font-weight: 600; color: {T['text']}; }}
    .card-value.up {{ color: {T['up']}; }}
    .card-value.down {{ color: {T['down']}; }}
    .card-close {{
      position: absolute; top: 10px; right: 14px;
      cursor: pointer; font-size: 1.1rem; color: {T['text_muted']};
      background: none; border: none; line-height: 1;
    }}
    .card-close:hover {{ color: {T['text']}; }}
    .legend {{
      display: flex; gap: 24px; margin-top: 16px;
      font-size: 0.78rem; color: {T['text_muted']};
    }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    .meta {{ margin-top: 20px; font-size: 0.72rem; color: {T['meta']}; }}
  </style>
</head>
<body>
<h1>{category} 트래픽 흐름</h1>
<p class="subtitle">{subtitle_steps} / 노드 클릭 시 상세 지표</p>
<div id="chart"></div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:{WEB_COLOR}"></div> Web</div>
  <div class="legend-item"><div class="legend-dot" style="background:{PC_COLOR}"></div> PC</div>
</div>

<div class="card-overlay" id="detailCard">
  <button class="card-close" onclick="closeCard()">✕</button>
  <h2 id="cardTitle"></h2>
  <div id="cardBody"></div>
</div>

<script>
const nodeData = {nodes_json};
const trace = {{
  type: 'sankey',
  orientation: 'h',
  arrangement: 'fixed',
  node: {{
    pad: 24, thickness: 28,
    line: {{ color: '{T['surface']}', width: 1.5 }},
    label: {node_labels_json},
    color: {node_colors_json},
    hovertemplate: '%{{label}}<extra></extra>'
  }},
  link: {{
    source: {sources_json},
    target: {targets_json},
    value: {values_json},
    color: {link_colors_json},
    customdata: {conv_json},
    hovertemplate: '전환율: %{{customdata}}<extra></extra>'
  }}
}};
const layout = {{
  paper_bgcolor: '{T['bg']}', plot_bgcolor: '{T['bg']}',
  font: {{ family: 'Noto Sans KR, Apple SD Gothic Neo, sans-serif', color: '{T['text']}', size: 13 }},
  height: 420, margin: {{ t: 20, b: 20, l: 10, r: 10 }}
}};
Plotly.newPlot('chart', [trace], layout, {{ responsive: true, displayModeBar: false }});

document.getElementById('chart').on('plotly_click', function(data) {{
  const pt = data.points[0];
  if (pt.index !== undefined && pt.index < nodeData.length) showCard(nodeData[pt.index]);
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
  if (d.conv) html += row('전환율', d.conv + (d.webConv ? ` / Web: ${{d.webConv}}` : '') + (d.pcConv ? ` / PC: ${{d.pcConv}}` : ''), 'up');
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
        description="CSV 트래픽 리포트 → Sankey HTML 생성기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/generate_sankey.py --csv docs/uv_report.csv --list
  python scripts/generate_sankey.py --csv docs/uv_report.csv --category 패키지
  python scripts/generate_sankey.py --csv docs/uv_report.csv --category 항공(해외) --output docs/항공_sankey.html
        """,
    )
    parser.add_argument("--csv", required=True, help="입력 CSV 경로")
    parser.add_argument("--category", help="시각화할 구분1 카테고리 (예: 패키지)")
    parser.add_argument("--output", help="출력 HTML 경로 (기본: docs/<category>_sankey.html)")
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
            if flow:
                print(f"  {c}  →  {' → '.join(flow)}  [흐름 정의 있음]")
            else:
                print(f"  {c}  [흐름 미정의 — CATEGORY_FLOWS에 추가 필요]")
        sys.exit(0)

    if not args.category:
        parser.error("--category 또는 --list 중 하나를 지정하세요.")

    category = args.category
    steps = CATEGORY_FLOWS.get(category)
    if not steps:
        print(f"오류: '{category}' 의 흐름 정의가 없습니다.", file=sys.stderr)
        print(f"  CATEGORY_FLOWS 에 추가하거나 --list 로 정의된 카테고리를 확인하세요.", file=sys.stderr)
        sys.exit(1)

    nodes = extract_nodes(rows, category, steps)
    if not nodes:
        print(f"오류: '{category}' 데이터를 CSV에서 추출할 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    html = render_html(category, nodes)

    if args.output:
        out_path = Path(args.output)
    else:
        safe_name = re.sub(r"[^\w]", "_", category, flags=re.UNICODE)
        out_path = csv_path.parent / f"{safe_name}_sankey.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print(f"생성 완료: {out_path}")
    print(f"  카테고리: {category}")
    print(f"  단계: {' → '.join(n['label'] for n in nodes)}")
    print(f"  노드 수: {len(nodes)}")


if __name__ == "__main__":
    main()
