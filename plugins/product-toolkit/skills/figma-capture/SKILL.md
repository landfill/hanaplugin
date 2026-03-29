---
name: figma-capture
description: 로컬 또는 외부 웹 페이지를 Figma로 html-to-design 캡처합니다. localhost/HTML 경로는 Chrome 해시 URL, 외부 https는 Chrome CDP 번들 스크립트를 사용합니다. "figma로 보내줘", "figma에 캡처", "figma-capture" 요청에 사용하세요.
argument-hint: "[localhost URL | HTML 파일 경로 | https 외부 URL] [선택: Figma 파일명]"
allowed-tools: Bash, Glob, Grep, Read, Edit, Write
---

# Figma Capture Skill

로컬 HTML 또는 **편집 불가한 외부 사이트**를 Figma 파일로 보내는 워크플로우입니다.

## 선행 조건

| 조건 | 설명 |
|------|------|
| **Figma MCP** | Cursor에 Figma MCP 서버가 설정되어 있어야 함 (서버명은 환경마다 다를 수 있음: `Figma`, `code_to_figma`, `user-code_to_figma` 등). `generate_figma_design` 도구로 captureId 발급 및 폴링에 사용. **이 MCP 없이는 LOCAL/EXTERNAL 모두 동작 불가.** |
| **Chrome** | 시스템에 Google Chrome 설치 필요 |
| **Node.js v22+** | EXTERNAL 캡처 시 CDP 스크립트 실행에 필요 (내장 WebSocket 사용) |

## Step -1: Figma MCP 연결 확인 (최초 1회)

스킬 실행 전 `generate_figma_design` 도구가 사용 가능한지 확인한다.

- **사용 가능** → Step 0으로 진행
- **사용 불가 (도구 미발견 또는 인증 오류)** → 아래 메시지를 사용자에게 안내하고 **스킬을 중단**:

> Figma MCP 서버가 연결되지 않았습니다.
> 1. **Cursor Settings → Features → MCP** 에서 Figma 서버가 등록되어 있는지 확인하세요.
> 2. 서버 옆 **Connect** 버튼을 클릭하여 브라우저 OAuth 인증을 완료하세요.
> 3. 인증 완료 후 이 스킬을 다시 실행해 주세요.

---

## Step 0: 대상 분류 (필수)

| 유형 | 조건 | 허용되는 캡처 방법 |
|------|------|-------------------|
| **LOCAL** | `http://localhost`, `127.0.0.1`, `*.local` 이거나, 레포에서 **편집 가능한 HTML**로 서빙 가능 | 아래 **LOCAL 전용** Step 1–6 (Chrome + `#figmacapture` 해시) |
| **EXTERNAL** | 그 외 `https://` (타 도메인, 수정 불가) | **EXTERNAL 전용 Step E1–E3** (Chrome CDP 번들 스크립트). 해시만 붙여 여는 방식은 **실패**함 |

**금지:** EXTERNAL에 대해 `https://example.com/...#figmacapture=...` 만으로 브라우저를 열지 말 것.

---

## EXTERNAL 전용: 외부 https URL

추가 설치 없이 Chrome CDP + 번들 Node.js 스크립트로 동작합니다 (Node.js v22+, Chrome 필요).

### Step E1: captureId 발급

**MCP 도구** (Cursor): Figma MCP 서버의 `generate_figma_design` 도구 사용
- 첫 호출: `outputMode` 없이 호출 → 플랜/파일 옵션 확인
- 둘째 호출: `outputMode: "existingFile"` + `fileKey` (또는 `newFile` + `fileName` / `planKey`)로 **captureId** 발급

### Step E2: 번들 스크립트로 캡처

이 스킬에 포함된 CDP 스크립트를 실행합니다. **Playwright, Puppeteer 등 추가 설치 불필요.**

실행 전 사용자에게 headless 여부를 확인:
- **headless (기본)**: 브라우저 창 없이 백그라운드 실행. 빠르고 깔끔함.
- **non-headless (`--no-headless`)**: 브라우저 창이 열려 캡처 과정을 직접 확인 가능. 디버깅이나 캡처 결과를 눈으로 확인하고 싶을 때 유용.

```bash
# headless (기본)
node <이 스킬 경로>/scripts/figma-capture-external.mjs \
  --url "https://example.com/page" \
  --capture-id "<captureId>"

# non-headless (브라우저 창 표시)
node <이 스킬 경로>/scripts/figma-capture-external.mjs \
  --url "https://example.com/page" \
  --capture-id "<captureId>" \
  --no-headless
```

스크립트 동작 흐름:
1. Chrome을 `--remote-debugging-port=9222`로 실행 (이미 실행 중이면 재사용)
2. CDP로 새 탭을 열어 외부 URL 탐색
3. CSP 우회 후 `capture.js` 주입
4. `window.figma.captureForDesign({captureId, endpoint, selector})` fire-and-forget 호출
5. 15초 대기 (캡처 데이터 네트워크 전송 완료) 후 탭 닫기

옵션: `--port <포트>` (기본 9222), `--timeout <초>` (기본 30), `--no-headless` (브라우저 창 표시)
### Step E3: 폴링

아래 [폴링 공통](#폴링-공통-mcp)과 동일. 새 captureId를 만들지 말 것.

> **참고:** EXTERNAL에서는 프로젝트 HTML에 `capture.js`를 직접 삽입할 수 없으므로 LOCAL Step 2는 건너뜁니다. CDP 스크립트가 런타임에 주입을 처리합니다.

---

## 입력 형식

- `http://localhost:8001/admin.html` — localhost URL
- `projects/4cut_review_manga/admin.html` — 프로젝트 내 HTML 경로 (→ LOCAL)
- `https://example.com/page` — 외부 사이트 (→ EXTERNAL)

---

## LOCAL 전용: 실행 순서

### Step 1: 입력 파싱

인자가 `http://localhost`로 시작하면 → **URL 모드**  
인자가 파일 경로이면 → **파일 경로 모드**

**파일 경로 모드:**

1. 파일 존재 확인  
2. 해당 폴더 서버 실행 여부:  
   - **Windows:** `netstat -ano | findstr :<port>`  
   - **macOS / Linux:** `lsof -i :<port>` 또는 `nc -z localhost <port> && echo open`  
3. 없으면 빈 포트(8001–8099)로 HTTP 서버:

```bash
python -m http.server <port> --directory "<folder>" &
sleep 2
```

4. `http://localhost:<port>/<filename>` 생성

### Step 2: HTML에 capture.js 삽입

대상 HTML을 Read로 읽고, `<head>` 안 **첫 번째 `<script>` 바로 앞**에 삽입:

```html
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js"></script>
```

- **`async` 없이** blocking `<script src>` 로 둔다 (해시 파라미터와 로드 순서 맞춤).  
- Figma MCP 예시에 `async`가 나와도, **이 스킬의 표준은 blocking**이다.  
- 이미 있으면 건너뜀.

### Step 3: Figma 출력 대상 + captureId

**MCP 매핑:** Figma MCP 서버의 **`generate_figma_design`** 도구를 사용한다 (서버명은 환경에 따라 다름).

1. **outputMode 없이** 한 번 호출 → 플랜/기존 파일 목록 등 옵션 수신  
2. 사용자 선택 또는 인자 매칭 후, **`outputMode` + `fileKey`** (또는 `newFile` 등)로 다시 호출 → **captureId** 획득

### Step 4: 브라우저로 캡처 URL 열기 (LOCAL만)

**Windows — Git Bash:**

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --incognito \
  "http://localhost:<port>/<page>?v=$(date +%s)#figmacapture=<captureId>&figmaendpoint=https%3A%2F%2Fmcp.figma.com%2Fmcp%2Fcapture%2F<captureId>%2Fsubmit&figmadelay=5000" &
```

**Windows — PowerShell (한 줄, URL은 실제 값으로 치환):**

```powershell
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' --incognito `
  'http://localhost:<port>/<page>?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() + '#figmacapture=<captureId>&figmaendpoint=https%3A%2F%2Fmcp.figma.com%2Fmcp%2Fcapture%2F<captureId>%2Fsubmit&figmadelay=5000'
```

Edge 사용 시 (PowerShell):

```powershell
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --inprivate '<위와 동일 URL>'
```

**macOS — Chrome 시크릿으로 URL 열기** (Git Bash 없이 터미널에서):

```bash
URL='http://localhost:<port>/<page>?v='$(date +%s)'#figmacapture=<captureId>&figmaendpoint=https%3A%2F%2Fmcp.figma.com%2Fmcp%2Fcapture%2F<captureId>%2Fsubmit&figmadelay=5000'
open -na "Google Chrome" --args --incognito "$URL"
```

또는 `open` 대신:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --incognito "$URL" &
```

**핵심:** `--incognito` / Edge는 `--inprivate`, `?v=` 캐시 버스트, `figmadelay=5000`, `start` / `Start-Process`로 URL 통째 전달 시 `&` 깨짐 주의 → **Chrome/Edge exe 직접 호출**  
브라우저 실행 후 **12초 대기** (`sleep 12` 또는 `Start-Sleep -Seconds 12`)

### 팀 공유 시 (Cursor / OS)

- **공유해도 됨.** 로직(LOCAL vs EXTERNAL, MCP, `capture.js`, 폴링)은 OS와 무관합니다.  
- **차이 나는 부분:** 포트 점검 명령, 브라우저 실행 경로(위 Windows / macOS 절).  
- **`.mcp.json`의 Figma MCP 서버 키**는 사람마다 다를 수 있음(예: `Figma`, `code_to_figma`). Cursor는 도구 이름에 `user-` 접두사를 붙이는 경우가 있으므로, **본인 환경의 MCP 목록에서 서버명을 확인**할 것.  
- **외부 URL:** `scripts/figma-capture-external.mjs`는 **Windows / macOS 공통** (Node.js v22+ 와 Chrome만 있으면 됨).

### Step 5–6: 폴링 및 완료

아래 [폴링 공통](#폴링-공통-mcp) 참고. 완료 후 capture.js는 HTML에 **유지** (제거 요청 시만 삭제). 임시 HTTP 서버를 켰다면 종료 여부 안내.

---

## 폴링 공통 (MCP)

`generate_figma_design`에 **`captureId`** 만 넘겨 상태 확인 (폴링 중 **새 captureId 생성 금지**).

권장 (MCP 설명과 정합):

- 간격 **5초**
- 최대 **10회** (필요 시 15회까지)

```
completed → Figma 링크 안내
pending / processing → 5초 대기 후 재시도
```

---

## 주의사항

- `file://` 는 지원하지 않음 → HTTP 서버 필요 (LOCAL)  
- 동일 captureId는 **1회만** 유효  
- LOCAL: capture.js는 blocking 로드 권장 (위 Step 2)  
- 이전에 실패한 captureId는 재발급  
- EXTERNAL: 반드시 번들 CDP 스크립트(`scripts/figma-capture-external.mjs`) 사용
