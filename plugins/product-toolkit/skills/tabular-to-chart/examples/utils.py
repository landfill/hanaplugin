#!/usr/bin/env python3
"""
utils.py
generate_funnel.py / generate_sankey.py 공통 유틸리티.
"""

import csv
import json
import re
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).parent
SCRIPTS_DIR = EXAMPLES_DIR.parent / "scripts"


def load_json(path: Path) -> dict:
    if not path.exists():
        print(f"오류: {path} 파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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
        return list(csv.DictReader(f))


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
