# Product Toolkit — Cursor 플러그인

프로덕트 기획자를 위한 Cursor 스킬 플러그인입니다.

## 포함 스킬

### 1. product-research (시장조사 & 기획)

- **시장조사**, **프로덕트 기획**, **아이디어 검증**, **사업계획**, **경쟁사 분석**, **MVP 기획**이 필요할 때 사용
- 8단계 인터뷰(페르소나별: 비즈니스/기획자, PM, 창업가) 후 맞춤형 리서치 프롬프트 생성

### 2. tagging-definition (태깅 정의서 자동 생성)

- **태깅 정의서 작성**, **이벤트 정의**, **프로퍼티 정의**, **Amplitude 태깅 기획**이 필요할 때 사용
- 대화형 인터뷰로 태깅 항목 수집 → 마크다운 데이터 파일 생성 → PPTX/XLSX 자동 변환
- 템플릿 기반 슬라이드 복제로 일관된 서식 보장, 프로젝트 루트 자동 탐지로 이미지 경로 무관하게 삽입

### 3. socrates (소크라테스식 기획 컨설팅)

- **바이브 코딩 입문자**, **아이디어 구체화**, **기획 문서 자동 생성**이 필요할 때 사용
- 소크라테스식 21문답으로 아이디어를 정제 → PRD·TRD·User Flow·DB 설계·디자인 시스템·코딩 컨벤션 6개 문서 자동 생성
- AI 코딩 파트너(Claude Code 등)가 즉시 개발을 시작할 수 있는 구조화된 기획 산출물 제공

### 4. tabular-to-chart (표 데이터 → 인터랙티브 차트)

- **CSV/Excel 데이터 시각화**, **차트 생성**, **보고서용 그래프**가 필요할 때 사용
- CSV·XLSX 파일 또는 클립보드 데이터를 파싱 → 바·라인·파이·산점도·히트맵·트리맵·산키·퍼널 등 8종 차트 생성
- Plotly.js 기반 인터랙티브 HTML 출력, `openpyxl` 의존성 자동 설치 지원 (Python 환경 없이도 안내 제공)

### 5. pdf-to-markdown (PDF → 마크다운 변환)

- **PDF 변환**, **PDF 텍스트 추출**, **PDF를 마크다운으로**, **PDF 파싱**이 필요할 때 사용
- opendataloader-pdf 기반으로 일반 디지털 PDF / 스캔 PDF / 한국어 OCR / 복잡한 표 등 4가지 모드 자동 선택
- Java·Python 환경 자동 점검 스크립트 포함, Hybrid 모드(OCR·수식·복잡한 표) 지원, 일괄 변환(배치) 가능

### 6. figma-capture (웹페이지 → Figma 캡처)

- **Figma로 보내줘**, **Figma에 캡처**, **HTML to Figma**, **웹페이지 Figma 변환**이 필요할 때 사용
- LOCAL(localhost/HTML 파일): Chrome 해시 URL + capture.js 방식으로 캡처
- EXTERNAL(외부 https): Chrome CDP 번들 스크립트로 headless 캡처 (Playwright 불필요, Node.js v22+ 내장 WebSocket 사용)
- 선행 조건: Chrome, Node.js v22+ (Figma MCP는 플러그인에 번들되어 자동 등록, 최초 1회 OAuth 인증 필요)

---

## 팀 마켓플레이스에 올리는 방법 (Cursor Enterprise / Teams)

Cursor **Teams**·**Enterprise** 플랜에서는 **팀 전용 마켓플레이스**에 이 플러그인을 올려 팀원이 공용으로 쓸 수 있습니다.

### 요구사항

- **Teams 플랜**: 팀 마켓플레이스 1개
- **Enterprise 플랜**: 팀 마켓플레이스 무제한

### 1단계: 이 폴더를 GitHub 저장소로 올리기

1. GitHub에 **새 저장소**를 만듭니다 (조직/팀 계정 권장).
2. 이 폴더 내용을 그 저장소에 푸시합니다.

   ```bash
   cd product-toolkit
   git init
   git add .
   git commit -m "프로덕트 기획 툴킷 플러그인 추가"
   git remote add origin https://github.com/YOUR_ORG/product-toolkit.git
   git push -u origin main
   ```

3. **Private** 저장소로 두면 팀 내부용, **Public**이면 공개용입니다. 팀 전용이면 Private 사용을 추천합니다.

### 2단계: Cursor 대시보드에서 팀 마켓플레이스에 Import

1. [Cursor Dashboard](https://cursor.com)에 로그인합니다.
2. **Settings → Plugins** 로 이동합니다.
3. **Team Marketplaces** 섹션을 찾습니다.  
   (없다면 아직 해당 계정에 팀 마켓플레이스가 활성화되지 않았을 수 있음)
4. **Import** 를 클릭합니다.
5. **마켓플레이스 이름·설명**을 입력하고 저장합니다.
6. **GitHub 저장소 URL**을 붙여넣고 Import를 완료합니다.  
   예: `https://github.com/landfill/hanaplugin`

### 3단계: 팀원이 플러그인 설치

- 팀 마켓플레이스가 연결되면, 팀원은 Cursor 설정의 **Rules, Skills** 또는 **Plugins**에서 팀 마켓플레이스를 보고 **product-toolkit** 플러그인을 설치할 수 있습니다.
- 채팅에서 "시장조사", "프로덕트 기획", "아이디어 검증", "태깅 정의서", "태깅 정의", "기획 컨설팅", "소크라테스", "차트 생성", "데이터 시각화", "PDF 변환", "PDF to markdown", "Figma로 보내줘", "Figma 캡처" 등으로 스킬이 자동 후보로 뜹니다.

---

## 알려진 이슈: 팀 마켓플레이스 Auto Refresh 미작동

> **상태**: Cursor 팀 확인·추적 중 (2026-03-16 공식 응답)

`Enable Auto Refresh`를 켜도 레포에 푸시한 스킬 추가/수정이 Cursor에 자동 반영되지 않는 [버그가 보고](https://forum.cursor.com/t/team-marketplace-auto-refresh-does-not-pick-up-plugin-changes-manual-refresh-cache-clear-reinstall-required/154675)되어 있습니다 (2026-03-13).

**업데이트를 반영하려면 아래 3단계를 수동으로 수행해야 합니다:**

```bash
# 1. 플러그인 캐시 삭제
rm -rf ~/.cursor/plugins/cache/<marketplace>/<plugin>/<ref>

# 2. Marketplace Settings → Plugin Repository → Refresh 클릭

# 3. 플러그인 언인스톨 후 재인스톨
```

---

## 참고 링크

- [Cursor Plugins 문서](https://cursor.com/docs/plugins)
- [팀 마켓플레이스 안내](https://cursor.com/docs/plugins#team-marketplaces)
- [플러그인 빌드 가이드](https://cursor.com/docs/plugins/building.md)
- [팀 마켓플레이스 Refresh 트러블슈팅 (포럼)](https://forum.cursor.com/t/team-marketplace-refresh-failing-since-mar-7-worked-fine-until-mar-6-public-repo-no-github-app-connected/154643) — 2.6 이후 `source` 경로 파싱 변경, 올바른 디렉터리 구조 등 해결 사례
- [Auto Refresh 미작동 버그 (포럼)](https://forum.cursor.com/t/team-marketplace-auto-refresh-does-not-pick-up-plugin-changes-manual-refresh-cache-clear-reinstall-required/154675) — 캐시 삭제 + Refresh + 재인스톨 워크어라운드
---

## 레포지토리 구조

```
├── .cursor-plugin/
│   └── marketplace.json          ← Team Marketplace 정의
├── plugins/
│   └── product-toolkit/
│       ├── .cursor-plugin/
│       │   └── plugin.json       ← 플러그인 메타데이터
│       ├── mcp.json               ← MCP 서버 설정 (Figma)
│       └── skills/
│           ├── product-research/
│           │   ├── SKILL.md
│           │   └── ...
│           ├── tagging-definition/
│           │   ├── SKILL.md
│           │   └── ...
│           └── socrates/
│               ├── SKILL.md
│               └── references/
│           ├── tabular-to-chart/
│           │   ├── SKILL.md
│           │   ├── scripts/
│           │   ├── examples/
│           │   └── references/
│           ├── pdf-to-markdown/
│           │   ├── SKILL.md
│           │   └── scripts/
│           └── figma-capture/
│               ├── SKILL.md
│               └── scripts/
├── .gitignore
└── README.md
```
