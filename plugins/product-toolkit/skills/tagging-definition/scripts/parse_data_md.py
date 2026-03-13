#!/usr/bin/env python3
"""
태깅 정의서 데이터 마크다운 파서.
reference.md의 "데이터 마크다운 형식"을 파싱하여 구조화된 dict 반환.
"""
import re
from pathlib import Path


def parse_md(path: str) -> dict:
    path = Path(path)
    text = path.read_text(encoding="utf-8")

    data = {
        "meta": {"서비스명": "", "팀": "", "작성자": "하니", "작성일": ""},
        "태깅 대상 화면": [],
        "이벤트": [],
    }

    # 메타정보
    meta_match = re.search(r"## 메타정보\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if meta_match:
        for line in meta_match.group(1).strip().split("\n"):
            m = re.match(r"-\s*(\S+):\s*(.+)", line.strip())
            if m:
                key, val = m.group(1).strip(), m.group(2).strip()
                if key in data["meta"]:
                    data["meta"][key] = val

    # 태깅 대상 화면
    scope_match = re.search(r"## 태깅 대상 화면\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if scope_match:
        for line in scope_match.group(1).strip().split("\n"):
            m = re.match(r"-\s*(.+)", line.strip())
            if m:
                data["태깅 대상 화면"].append(m.group(1).strip())

    # 이벤트
    events_block = re.search(r"## 이벤트\s*\n(.*)", text, re.DOTALL)
    if events_block:
        block = events_block.group(1)
        # ### 이벤트 N ... 다음 ### 또는 끝까지
        event_sections = re.split(r"\n###\s+", block)
        for sec in event_sections:
            sec = sec.strip()
            if not sec:
                continue
            lines = sec.split("\n")
            event = {
                "호출 시점": "",
                "Event Name (영문)": "",
                "Event Name (한글)": "",
                "캡처 경로": "",
                "properties": [],
            }
            in_table = False
            table_header = None
            for line in lines:
                line_stripped = line.strip()
                if line_stripped.startswith("|") and "---" in line_stripped:
                    continue  # 구분선 행은 스킵, in_table 유지
                if line_stripped.startswith("|"):
                    parts = [c.strip() for c in line.split("|") if c.strip()]
                    if not in_table:
                        table_header = parts
                        in_table = True
                        continue
                    if len(parts) >= 4 and table_header:
                        event["properties"].append({
                            "Event property": parts[0],
                            "property 구분": parts[1],
                            "value": parts[2],
                            "description": parts[3],
                        })
                    continue
                in_table = False
                m = re.match(r"-\s*(.+?):\s*(.+)", line.strip())
                if m:
                    key, val = m.group(1).strip(), m.group(2).strip()
                    if key in event:
                        event[key] = val
            if event["Event Name (영문)"] or event["Event Name (한글)"] or event["properties"]:
                data["이벤트"].append(event)

    return data
