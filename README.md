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
- 채팅에서 "시장조사", "프로덕트 기획", "아이디어 검증", "태깅 정의서", "태깅 정의", "기획 컨설팅", "소크라테스" 등으로 스킬이 자동 후보로 뜹니다.

---

## 참고 링크

- [Cursor Plugins 문서](https://cursor.com/docs/plugins)
- [팀 마켓플레이스 안내](https://cursor.com/docs/plugins#team-marketplaces)
- [플러그인 빌드 가이드](https://cursor.com/docs/plugins/building.md)

---

## 플러그인 구조

```
├── .cursor-plugin/
│   └── plugin.json
├── skills/
│   ├── product-research/
│   │   ├── SKILL.md
│   │   ├── questions-business.md
│   │   ├── questions-pm.md
│   │   ├── questions-founder.md
│   │   └── research-prompt-template.md
│   ├── tagging-definition/
│   │   ├── SKILL.md
│   │   ├── reference.md
│   │   ├── template/
│   │   │   └── 태깅정의서_템플릿.pptx
│   │   └── scripts/
│   │       ├── run_generate.py
│   │       ├── generate_pptx.py
│   │       ├── generate_xlsx.py
│   │       ├── parse_data_md.py
│   │       ├── requirements.txt
│   │       └── 태깅정의_데이터_샘플.md
│   └── socrates/
│       ├── SKILL.md
│       └── references/
│           ├── questions.md
│           ├── conversation-rules.md
│           ├── prd-template.md
│           ├── trd-template.md
│           ├── user-flow-template.md
│           ├── database-design-template.md
│           ├── design-system-template.md
│           ├── coding-convention-template.md
│           ├── tasks-template.md
│           └── tasks-generation-rules.md
├── .gitignore
└── README.md
```
