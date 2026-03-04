# Product Research — Cursor 플러그인

프로덕트 아이디어를 체계적인 시장조사 및 기획서로 발전시키는 Cursor 스킬 플러그인입니다.

## 스킬 설명

- **시장조사**, **프로덕트 기획**, **아이디어 검증**, **사업계획**, **경쟁사 분석**, **MVP 기획**이 필요할 때 사용
- 8단계 인터뷰(페르소나별: 비즈니스/기획자, PM, 창업가) 후 맞춤형 리서치 프롬프트 생성

---

## 팀 마켓플레이스에 올리는 방법 (Cursor Enterprise / Teams)

Cursor **Teams**·**Enterprise** 플랜에서는 **팀 전용 마켓플레이스**에 이 플러그인을 올려 팀원이 공용으로 쓸 수 있습니다.

### 요구사항

- **Teams 플랜**: 팀 마켓플레이스 1개
- **Enterprise 플랜**: 팀 마켓플레이스 무제한

### 1단계: 이 폴더를 GitHub 저장소로 올리기

1. GitHub에 **새 저장소**를 만듭니다 (조직/팀 계정 권장).
2. 이 폴더(`cursor-plugin-product-research/`) 내용을 그 저장소에 푸시합니다.

   ```bash
   cd cursor-plugin-product-research
   git init
   git add .
   git commit -m "프로덕트 시장조사 스킬 플러그인 추가"
   git remote add origin https://github.com/YOUR_ORG/product-research-plugin.git
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
   예: `https://github.com/YOUR_ORG/product-research-plugin`

### 3단계: 팀원이 플러그인 설치

- 팀 마켓플레이스가 연결되면, 팀원은 Cursor 설정의 **Rules, Skills** 또는 **Plugins**에서 팀 마켓플레이스를 보고 **product-research** 플러그인을 설치할 수 있습니다.
- 채팅에서 "시장조사", "프로덕트 기획", "아이디어 검증" 등으로 스킬이 자동 후보로 뜹니다.

---

## 참고 링크

- [Cursor Plugins 문서](https://cursor.com/docs/plugins)
- [팀 마켓플레이스 안내](https://cursor.com/docs/plugins#team-marketplaces)
- [플러그인 빌드 가이드](https://cursor.com/docs/plugins/building.md)

---

## 플러그인 구조

```
cursor-plugin-product-research/
├── .cursor-plugin/
│   └── plugin.json
├── skills/
│   └── product-research/
│       ├── SKILL.md
│       ├── questions-business.md
│       ├── questions-pm.md
│       ├── questions-founder.md
│       └── research-prompt-template.md
└── README.md
```

`plugin.json`의 `author.name`은 팀/조직 이름으로 바꿔서 사용하면 됩니다.
