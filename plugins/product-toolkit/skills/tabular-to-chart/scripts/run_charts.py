#!/usr/bin/env python3
"""
run_charts.py
tabular-to-chart 스킬 런타임 진입점.

- openpyxl 이 없으면 venv를 자동 생성하고 설치한 뒤 재실행한다.
- parse_tabular.py / generate_chart.py 는 표준 라이브러리만 사용하므로
  별도 설치 없이 바로 실행된다.
- openpyxl 은 복잡한 xlsx(병합셀·수식) 파싱에만 필요하다.

사용법:
  # 차트 생성 (generate_chart.py 래퍼)
  python3 run_charts.py chart --config chart_config.json
  python3 run_charts.py chart --config chart_config.json --output result.html
  python3 run_charts.py chart --list-types

  # 테이블 파싱 (parse_tabular.py 래퍼)
  python3 run_charts.py parse --file data.xlsx --summary
  python3 run_charts.py parse --file data.xlsx --list-sheets
  python3 run_charts.py parse --file data.xlsx --sheet "매출" --to-csv output.csv
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VENV_DIR = SCRIPT_DIR / ".venv"


def _venv_python() -> Path:
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python3"


def _in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def _install_openpyxl():
    """openpyxl 을 venv에 설치하고 venv Python으로 재실행한다."""
    if _in_venv():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "openpyxl"],
            check=True,
        )
        return

    venv_py = _venv_python()
    if not venv_py.exists():
        print("venv 생성 중...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)

    subprocess.run(
        [str(venv_py), "-m", "pip", "install", "-q", "openpyxl"],
        check=True,
    )
    os.execv(str(venv_py), [str(venv_py)] + sys.argv)


def ensure_openpyxl_if_needed():
    """stdlib xlsx 파서가 실패할 때만 openpyxl 설치를 시도한다.

    parse_tabular.py 는 stdlib 파서를 먼저 시도하고 실패 시 openpyxl 을 임포트한다.
    run_charts.py 는 파일 확장자만 보고 미리 설치하지 않는다 — stdlib 파서가
    성공하면 설치가 전혀 불필요하기 때문이다.
    openpyxl 이 필요해지는 시점(ImportError)은 parse_tabular.py 내부에서 발생하므로,
    여기서는 이미 설치된 경우만 조용히 통과하고 미설치 상태를 그대로 둔다.
    실제 설치 트리거는 parse_tabular._xlsx_to_rows_openpyxl() 의 ImportError 경로에서
    사용자에게 안내 메시지를 출력한다.
    """
    # 아무것도 하지 않는다 — parse_tabular.py 가 자체적으로 처리한다.
    pass


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "사용법:\n"
            "  python3 run_charts.py chart --config chart_config.json [--output result.html]\n"
            "  python3 run_charts.py chart --list-types\n"
            "  python3 run_charts.py parse --file data.xlsx --summary\n"
            "  python3 run_charts.py parse --file data.xlsx --list-sheets\n"
            "  python3 run_charts.py parse --file data.xlsx --sheet '매출' --to-csv output.csv",
            file=sys.stderr,
        )
        sys.exit(1)

    subcommand = sys.argv[1].lower()
    rest = sys.argv[2:]

    if subcommand == "chart":
        # generate_chart.py 는 표준 라이브러리만 사용 — 설치 불필요
        sys.argv = [str(SCRIPT_DIR / "generate_chart.py")] + rest
        exec(compile((SCRIPT_DIR / "generate_chart.py").read_text(encoding="utf-8"),
                     str(SCRIPT_DIR / "generate_chart.py"), "exec"),
             {"__name__": "__main__", "__file__": str(SCRIPT_DIR / "generate_chart.py")})

    elif subcommand == "parse":
        # openpyxl 은 parse_tabular.py 내부에서 필요 시 자체 처리한다.
        # run_charts.py 는 미리 설치하지 않는다 — stdlib 파서가 성공하면 불필요.
        sys.argv = [str(SCRIPT_DIR / "parse_tabular.py")] + rest
        exec(compile((SCRIPT_DIR / "parse_tabular.py").read_text(encoding="utf-8"),
                     str(SCRIPT_DIR / "parse_tabular.py"), "exec"),
             {"__name__": "__main__", "__file__": str(SCRIPT_DIR / "parse_tabular.py")})

    else:
        print(f"오류: 알 수 없는 서브커맨드 — '{subcommand}'. chart 또는 parse 를 사용하세요.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
