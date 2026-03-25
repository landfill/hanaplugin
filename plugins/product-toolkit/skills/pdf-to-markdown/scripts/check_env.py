#!/usr/bin/env python3
"""
PDF to Markdown 스킬 - 환경 점검 스크립트
Java, Python, opendataloader-pdf 설치 여부를 확인하고 JSON으로 출력한다.
"""

import json
import subprocess
import sys


def check_java():
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stderr or result.stdout
        version_line = output.splitlines()[0] if output else ""
        version = version_line.split('"')[1] if '"' in version_line else "unknown"
        major = int(version.split(".")[0]) if version != "unknown" else 0
        return {"installed": result.returncode == 0, "version": version, "ok": major >= 11}
    except (FileNotFoundError, subprocess.TimeoutExpired, IndexError, ValueError):
        return {"installed": False, "version": None, "ok": False}


def check_python():
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = sys.version_info >= (3, 10)
    return {"installed": True, "version": version, "ok": ok}


def check_opendataloader():
    try:
        import importlib
        spec = importlib.util.find_spec("opendataloader_pdf")
        if spec is None:
            return {"installed": False, "hybrid": False}
        import opendataloader_pdf
        version = getattr(opendataloader_pdf, "__version__", "unknown")

        hybrid = False
        try:
            result = subprocess.run(
                ["opendataloader-pdf-hybrid", "--help"],
                capture_output=True, timeout=5
            )
            hybrid = result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return {"installed": True, "version": version, "hybrid": hybrid}
    except Exception:
        return {"installed": False, "hybrid": False}


def main():
    java = check_java()
    python = check_python()
    odl = check_opendataloader()

    issues = []
    if not java["installed"]:
        issues.append("Java가 설치되지 않았습니다 (Java 11+ 필요)")
    elif not java["ok"]:
        issues.append(f"Java 버전이 낮습니다 ({java['version']}, 11+ 필요)")
    if not python["ok"]:
        issues.append(f"Python 버전이 낮습니다 ({python['version']}, 3.10+ 필요)")
    if not odl["installed"]:
        issues.append("opendataloader-pdf가 설치되지 않았습니다")

    result = {
        "java": java["installed"],
        "java_version": java["version"],
        "java_ok": java["ok"],
        "python": python["installed"],
        "python_version": python["version"],
        "python_ok": python["ok"],
        "opendataloader": odl["installed"],
        "opendataloader_version": odl.get("version"),
        "hybrid": odl["hybrid"],
        "issues": issues,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
