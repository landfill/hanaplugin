---
name: pdf-to-markdown
description: >-
  PDF 파일을 마크다운으로 변환한다. opendataloader-pdf 라이브러리를 사용하며
  Java/Python 환경 자동 점검, 일반/스캔/한국어/복잡한 표 PDF 모드 자동 선택을 지원한다.
  사용자가 PDF 변환, PDF를 마크다운으로, PDF 텍스트 추출, pdf convert, pdf to markdown,
  pdf to md, extract text from pdf, convert pdf, PDF 읽기, PDF 파싱 등을 언급하면 이 스킬을 사용한다.
  PDF 파일 경로가 대화에 등장하거나 PDF 관련 작업을 요청받으면 반드시 이 스킬을 참고한다.
---

# PDF to Markdown

opendataloader-pdf를 사용해 PDF를 마크다운으로 변환한다.

## 질문 인터페이스 규칙

사용자에게 묻는 **모든 질문**은 **구조화된 선택지 UI**로 제시한다.
일반 채팅 텍스트만으로 "어떤 걸로 할까요?"라고 하지 않는다.
한 번에 하나의 질문만 한다. 여러 질문을 몰아서 하지 않는다.

- 각 질문에는 **선택지(options)**를 반드시 포함한다.
- 자유입력이 필요한 경우에도 선택지 중 하나로 **"직접 입력"** 또는 **"기타 (직접 입력)"**을 둔다.
- 예외 없이 적용한다.

### 질문 도구 우선순위 (Fallback Chain)

**스킬 시작 시 1회만** 사용 가능한 도구를 감지하고, **세션 전체에서 동일 도구**를 사용한다.
매 질문마다 도구를 다시 감지하지 않는다.

| 순위 | 도구 | 환경 | 조건 |
|------|------|------|------|
| 1 | `AskQuestion` | Cursor 네이티브 | 컨텍스트에 사용 가능한 경우 |
| 2 | `AskUserQuestion` | Claude Code 네이티브 | AskQuestion이 없을 때 |
| 3 | 마크다운 텍스트 | 범용 | 두 도구 모두 없을 때 |

순위 3(마크다운 텍스트)을 사용하는 경우, 선택지를 번호/알파벳 목록으로 표시하고 사용자 응답을 기다린다.

---

## 워크플로우

### Step 0: OS 감지

OS를 감지하고 세션 전체에서 해당 OS에 맞는 명령어를 사용한다.

- macOS/Linux: `uname -s`
- Windows: 환경변수 `OS` 확인 또는 `$env:OS` (PowerShell)

이하 모든 명령어 예시에서 `[macOS/Linux]`와 `[Windows]`로 구분 표기한다.

### Step 1: 환경 점검

**반드시 점검을 먼저 수행하고 그 결과를 확인한 뒤에만 다음 판단을 내린다.**
점검하지 않고 사용자에게 설치 여부를 묻거나 추측하지 않는다.

#### 1-A. Python이 있는 경우

터미널에서 `python3 --version` (macOS/Linux) 또는 `python --version` (Windows)을 실행한다.
정상 출력되면 Python이 있으므로 `check_env.py`를 실행한다:

```bash
# [macOS/Linux]
python3 <skill_dir>/scripts/check_env.py

# [Windows]
python <skill_dir>\scripts\check_env.py
```

스크립트 JSON 출력 예시:
```json
{
  "java": true, "java_version": "17.0.9", "java_ok": true,
  "python": true, "python_version": "3.11.4", "python_ok": true,
  "opendataloader": true, "opendataloader_version": "2.0.2",
  "hybrid": false, "issues": []
}
```

**`issues`가 비어 있으면 (`[]`) 환경 준비 완료 → 즉시 Step 2로 진행한다.**
`issues`에 항목이 있을 때만 아래 해결 분기를 따른다.

#### 1-B. Python이 없는 경우 (명령어 실행 실패)

`check_env.py`를 실행할 수 없으므로 직접 점검한다:

1. **Java 점검**: `java -version` 실행
2. **opendataloader-pdf**: Python 없이는 사용 불가 → Python 설치가 선행 필수

`AskQuestion`으로 Python 설치 안내:

| 선택 | 동작 |
|------|------|
| A) 직접 설치 후 진행 | 아래 안내 출력 후 재점검 대기 |
| B) 자동 설치 시도 | OS별 명령어 실행 |
| C) 중단 | 스킬 종료 |

**Python 설치 명령어:**
- macOS: `brew install python3` 또는 https://python.org
- Windows: `winget install Python.Python.3.12` 또는 https://python.org
- Linux: `sudo apt install python3` / `sudo dnf install python3`

Python 설치 완료 후 Step 1-A로 돌아가 `check_env.py`를 실행한다.

#### 환경 문제 해결 분기

##### Java 미설치 또는 버전 부족 (`java_ok: false`)

`AskQuestion`으로 선택지 제시:

| 선택 | 동작 |
|------|------|
| A) 직접 설치 후 진행 | OS별 안내 출력 후 재점검 대기 |
| B) 자동 설치 시도 | OS별 명령어 실행 |
| C) 중단 | 스킬 종료 |

**Java 설치 명령어 (11 이상 필요):**
- macOS: `brew install --cask temurin`
- Windows: `winget install EclipseAdoptium.Temurin.21.JDK`
- Linux: `sudo apt install temurin-21-jdk`
- 공통: https://adoptium.net

##### opendataloader-pdf 미설치 (`opendataloader: false`)

`AskQuestion`으로 선택지 제시:

| 선택 | 동작 |
|------|------|
| A) 기본 설치 | `pip install -U opendataloader-pdf` |
| B) Hybrid 모드 포함 설치 | `pip install -U "opendataloader-pdf[hybrid]"` |
| C) 중단 | 스킬 종료 |

> Hybrid 모드: 복잡한 표, 스캔 PDF, OCR, 수식 지원. 약 500MB 추가 설치.

---

### Step 2: PDF 경로 확인

사용자가 PDF 경로를 이미 제공했으면 그대로 사용한다.
경로가 없으면 `AskQuestion`으로 요청한다:
- 선택지: 현재 열린 파일 목록 + "직접 입력"

---

### Step 3: PDF 유형 판별

`AskQuestion`으로 PDF 유형을 묻는다:

| 선택 | 설명 | 사용 모드 |
|------|------|----------|
| A) 일반 디지털 PDF | 텍스트 선택 가능한 PDF | 기본 모드 |
| B) 스캔된 PDF | 이미지 기반, 텍스트 선택 불가 | Hybrid + OCR |
| C) 한국어 포함 스캔 PDF | 한국어 OCR 필요 | Hybrid + OCR (ko,en) |
| D) 복잡한 표가 있는 PDF | 병합 셀, 테두리 없는 표 | Hybrid |
| E) 잘 모르겠음 | 자동 감지 | 아래 자동 감지 로직 참고 |

#### 자동 감지 로직 (E 선택 시)

1. 기본 모드로 변환을 시도한다.
2. 결과 마크다운이 비어 있거나 텍스트가 극히 적으면(공백 제외 100자 미만), 스캔 PDF일 가능성이 높다.
3. 이 경우 Hybrid 설치 여부를 확인하고:
   - 설치됨 → Hybrid + OCR 모드로 재시도
   - 미설치 → 사용자에게 "스캔 PDF로 보입니다. Hybrid 모드를 설치하면 OCR 변환이 가능합니다. 설치할까요?" 안내
4. 기본 모드 결과가 충분하면 그대로 사용한다.

---

### Step 3.5: 이미지 처리 옵션

`AskQuestion`으로 이미지 처리 방식을 묻는다:

| 선택 | 설명 | `image_output` 값 |
|------|------|-------------------|
| A) 이미지 제외 | 텍스트만 추출 (로고, 아이콘, 사진 모두 제외) | `"off"` |
| B) 이미지 별도 저장 | 이미지를 파일로 저장하고 마크다운에서 참조 (기본값) | `"external"` |
| C) 이미지 인라인 포함 | Base64로 마크다운에 직접 삽입 | `"embedded"` |

> 대부분의 문서 변환에서는 **A) 이미지 제외**가 깔끔하다.
> 차트나 도표처럼 내용에 중요한 이미지가 있는 경우에만 B 또는 C를 선택한다.

---

### Step 4: 변환 실행

출력 경로: `{PDF가 있는 폴더}/output/`

#### 기본 모드 (A 또는 자동 감지 첫 시도)

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["<pdf_path>"],
    output_dir="<pdf_dir>/output/",
    format="markdown",
    image_output="<Step 3.5에서 선택한 값>"
)
```

#### Hybrid 모드 (B, C, D)

Hybrid 패키지 설치 여부를 먼저 확인한다(`hybrid: true` in check_env 결과).
미설치 시 `pip install -U "opendataloader-pdf[hybrid]"` 설치를 제안한다.

**백엔드 서버를 백그라운드로 시작한 뒤 변환을 실행한다.**

서버 시작 (유형에 따라 옵션 선택):

```bash
# [macOS/Linux]
# B) 스캔 PDF
nohup opendataloader-pdf-hybrid --port 5002 --force-ocr > /dev/null 2>&1 &
HYBRID_PID=$!
# C) 한국어 스캔 PDF
nohup opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "ko,en" > /dev/null 2>&1 &
HYBRID_PID=$!
# D) 복잡한 표
nohup opendataloader-pdf-hybrid --port 5002 > /dev/null 2>&1 &
HYBRID_PID=$!

# [Windows PowerShell]
# B) 스캔 PDF
$proc = Start-Process -NoNewWindow -PassThru opendataloader-pdf-hybrid -ArgumentList "--port 5002 --force-ocr"
# C) 한국어 스캔 PDF
$proc = Start-Process -NoNewWindow -PassThru opendataloader-pdf-hybrid -ArgumentList "--port 5002 --force-ocr --ocr-lang ko,en"
# D) 복잡한 표
$proc = Start-Process -NoNewWindow -PassThru opendataloader-pdf-hybrid -ArgumentList "--port 5002"
```

서버 준비 대기 (최대 30초):

```bash
# [macOS/Linux]
for i in $(seq 1 30); do
  curl -s http://localhost:5002/health > /dev/null 2>&1 && break
  sleep 1
done

# [Windows PowerShell]
for ($i=1; $i -le 30; $i++) {
  try { Invoke-WebRequest -Uri http://localhost:5002/health -UseBasicParsing -ErrorAction Stop | Out-Null; break } catch { Start-Sleep 1 }
}
```

변환 실행:
```python
opendataloader_pdf.convert(
    input_path=["<pdf_path>"],
    output_dir="<pdf_dir>/output/",
    format="markdown",
    hybrid="docling-fast",
    image_output="<Step 3.5에서 선택한 값>"
)
```

변환 완료 후 서버 정리:
```bash
# [macOS/Linux]
kill $HYBRID_PID 2>/dev/null

# [Windows PowerShell]
Stop-Process -Id $proc.Id -ErrorAction SilentlyContinue
```

---

### Step 5: 후처리 및 결과 안내

#### 마크다운 정리

변환된 마크다운에 불필요한 HTML 태그(`<br>`, `<br/>`)가 포함될 수 있다.
변환 완료 후 출력 파일에서 정리를 수행한다.

Python으로 처리한다 (OS 무관):
```python
import re
from pathlib import Path

output = Path("<output_file>")
text = output.read_text(encoding="utf-8")
text = re.sub(r"<br\s*/?>", "\n", text)
# 연속 빈 줄 3개 이상을 2개로 축소
text = re.sub(r"\n{3,}", "\n\n", text)
output.write_text(text, encoding="utf-8")
```

#### 결과 안내

변환 완료 후:
```
변환 완료
입력: /path/to/파일.pdf
출력: /path/to/output/파일.md
```

#### 에러 대응

| 에러 유형 | 증상 | 대응 |
|----------|------|------|
| Java 메모리 부족 | `OutOfMemoryError` | 환경변수 `_JAVA_OPTIONS="-Xmx4g"` 설정 후 재시도 |
| 암호화된 PDF | `Password required` 또는 `encrypted` | 사용자에게 비밀번호 요청 또는 비밀번호 없는 PDF 준비 안내 |
| 손상된 PDF | `Invalid PDF` 또는 파싱 에러 | PDF 손상 안내. 다른 뷰어에서 열리는지 확인 요청 |
| Hybrid 서버 미응답 | `Connection refused` on port 5002 | 서버 재시작 시도. 포트 충돌 확인: macOS/Linux `lsof -i :5002`, Windows `netstat -ano | findstr :5002` |
| 빈 결과물 | 마크다운 파일이 비어 있음 | 스캔 PDF일 가능성 → Hybrid + OCR 모드 제안 |

그 외 에러는 에러 메시지를 그대로 출력하고 원인을 분석해 안내한다.

---

## 일괄 변환 (배치)

여러 파일 또는 폴더 전체를 변환할 때:

```python
opendataloader_pdf.convert(
    input_path=["file1.pdf", "file2.pdf", "폴더경로/"],
    output_dir="output/",
    format="markdown"
)
```

> `convert()`는 호출마다 JVM을 새로 생성하므로 반드시 **한 번에 배치로 처리**한다.

---

## 추가 옵션

| 옵션 | 설명 |
|------|------|
| `image_output="off"` | 이미지 완전 제외 (텍스트만 추출) |
| `image_output="external"` | 이미지를 별도 파일로 저장 (기본값) |
| `image_output="embedded"` | 이미지를 Base64로 마크다운에 인라인 포함 |
| `image_format="png"` | 이미지 저장 형식: `"png"` (기본값) 또는 `"jpeg"` |
| `format="markdown,json"` | 마크다운 + JSON 동시 출력 |
| `use_struct_tree=True` | Tagged PDF의 구조 태그 활용 |
| `content_safety_off="tiny"` | 작은 이미지(로고/아이콘) 자동 필터 해제 (기본: 필터 활성) |
