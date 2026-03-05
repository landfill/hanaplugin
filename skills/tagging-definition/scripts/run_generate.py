#!/usr/bin/env python3
"""
스킬 런타임용 진입점. 의존성(python-pptx, openpyxl)이 없으면 자동 설치한 뒤
generate_pptx 또는 generate_xlsx를 실행한다. 사용자가 미리 pip install 할 필요 없다.

사용법:
  python3 run_generate.py pptx <데이터.md> <출력.pptx> [템플릿.pptx]
  python3 run_generate.py xlsx <데이터.md> <출력.xlsx>
"""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REQUIREMENTS = SCRIPT_DIR / "requirements.txt"


def ensure_deps():
    """필요 패키지가 없으면 requirements.txt 기준으로 설치."""
    try:
        import pptx  # noqa: F401
        import openpyxl  # noqa: F401
        return True
    except ImportError:
        pass
    if not REQUIREMENTS.exists():
        for pkg in ("python-pptx", "openpyxl"):
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", pkg],
                check=False,
            )
        return True
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS)],
        check=True,
    )
    return True


def main():
    if len(sys.argv) < 4:
        print(
            "사용법: python3 run_generate.py pptx <데이터.md> <출력.pptx> [템플릿.pptx]\n"
            "       python3 run_generate.py xlsx <데이터.md> <출력.xlsx>",
            file=sys.stderr,
        )
        sys.exit(1)
    kind = sys.argv[1].lower()
    if kind not in ("pptx", "xlsx"):
        print("첫 인자는 pptx 또는 xlsx 여야 합니다.", file=sys.stderr)
        sys.exit(1)
    ensure_deps()
    # 하위 스크립트가 기대하는 argv: [스크립트명, 데이터.md, 출력경로, ...]
    orig_argv = sys.argv
    sys.argv = [orig_argv[0], orig_argv[2], orig_argv[3]] + (orig_argv[4:] if len(orig_argv) > 4 else [])
    if kind == "pptx":
        from generate_pptx import main as run_pptx
        run_pptx()
    else:
        from generate_xlsx import main as run_xlsx
        run_xlsx()


if __name__ == "__main__":
    main()
