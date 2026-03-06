#!/usr/bin/env python3
"""
스킬 런타임용 진입점. 의존성(python-pptx, openpyxl)이 없으면 venv를 자동 생성하고
의존성을 설치한 뒤 generate_pptx 또는 generate_xlsx를 실행한다.
사용자가 미리 pip install 할 필요 없다.

PEP 668(externally-managed-environment) 환경(macOS Homebrew 등)에서도
시스템 Python에 직접 pip install하지 않고 venv를 통해 안전하게 동작한다.

사용법:
  python3 run_generate.py pptx <데이터.md> <출력.pptx> [템플릿.pptx]
  python3 run_generate.py xlsx <데이터.md> <출력.xlsx>
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REQUIREMENTS = SCRIPT_DIR / "requirements.txt"
VENV_DIR = SCRIPT_DIR / ".venv"


def _venv_python() -> Path:
    """venv 내 Python 실행 파일 경로를 반환한다."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python3"


def _in_venv() -> bool:
    """현재 프로세스가 venv 안에서 실행 중인지 확인한다."""
    return sys.prefix != sys.base_prefix


def ensure_deps():
    """필요 패키지가 없으면 venv를 생성하고 의존성을 설치한 뒤 venv Python으로 재실행한다."""
    try:
        import pptx  # noqa: F401
        import openpyxl  # noqa: F401
        return
    except ImportError:
        pass

    if _in_venv():
        req_args = [sys.executable, "-m", "pip", "install", "-q"]
        if REQUIREMENTS.exists():
            req_args += ["-r", str(REQUIREMENTS)]
        else:
            req_args += ["python-pptx", "openpyxl"]
        subprocess.run(req_args, check=True)
        return

    venv_py = _venv_python()
    if not venv_py.exists():
        print("venv 생성 중...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)

    req_args = [str(venv_py), "-m", "pip", "install", "-q"]
    if REQUIREMENTS.exists():
        req_args += ["-r", str(REQUIREMENTS)]
    else:
        req_args += ["python-pptx", "openpyxl"]
    subprocess.run(req_args, check=True)

    os.execv(str(venv_py), [str(venv_py)] + sys.argv)


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
