# SeungBeom.dev 프로젝트 가이드

## 1. 기술 스택

| 기술 | 용도 |
|------|------|
| Jekyll + Chirpy 테마 | 정적 사이트 생성 |
| GitHub Pages | 호스팅 |
| GitHub Actions | CI/CD 자동화 |
| Groq API + LLaMA 3.3 | AI 글 생성 |
| Giscus | 댓글 시스템 |
| GoatCounter | 방문 통계 |

---

## 2. 폴더 구조

```
HyunSeungBeom.github.io/
├── _config.yml              # 사이트 전체 설정
├── _posts/                  # 블로그 게시물 (마크다운)
├── _tabs/                   # 상단 메뉴 (About, Archives 등)
├── _data/                   # 사이트 데이터 (언어, 공유버튼 등)
├── _includes/               # 재사용 HTML 조각
├── assets/                  # 이미지, CSS, JS
│   └── img/avatar.png       # 프로필 이미지
├── scripts/
│   └── generate_cs_post.py  # AI 게시물 자동 생성 스크립트
└── .github/workflows/
    ├── pages-deploy.yml     # 빌드 & 배포 워크플로우
    └── daily-cs-post.yml    # 매일 자동 게시물 생성
```

---

## 3. 자동화 흐름

### 매일 자동 게시물 생성 (오전 8시 KST)

```
┌──────────────────────────────────────────────────────────────┐
│                     매일 오전 8시 (KST)                       │
│                   cron: '0 23 * * *' (UTC)                   │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│            GitHub Actions: daily-cs-post.yml                 │
├──────────────────────────────────────────────────────────────┤
│  1. Checkout & Pull (최신 상태 동기화)                        │
│  2. Python 스크립트 실행 (generate_cs_post.py)               │
│     ├─ 기존 게시물 확인 → 중복 주제 제외                      │
│     ├─ Groq API로 글 생성 (LLaMA 3.3)                        │
│     ├─ 외국어 필터링 (중국어/일본어/힌디어 자동 제거)          │
│     └─ _posts/YYYY-MM-DD-주제.md 파일 생성                   │
│  3. Git commit & push                                        │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│            GitHub Actions: pages-deploy.yml                  │
│                    (push 시 자동 트리거)                      │
├──────────────────────────────────────────────────────────────┤
│  1. Jekyll 빌드 (_posts 마크다운 → HTML)                     │
│  2. HTML 검증 (htmlproofer)                                  │
│  3. GitHub Pages에 배포                                      │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│          https://hyunseungbeom.github.io 에 반영             │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. 주요 설정 (_config.yml)

### 기본 설정
```yaml
title: SeungBeom.dev
tagline: "매일 성장하는 개발자의 기록"
url: "https://hyunseungbeom.github.io"
timezone: Asia/Seoul
lang: ko-KR
future: true  # 시간대 차이로 인한 게시물 누락 방지
```

### 댓글 (Giscus)
```yaml
comments:
  provider: giscus
  giscus:
    repo: HyunSeungBeom/HyunSeungBeom.github.io
    repo_id: R_kgDOQ63F_Q
    category: Announcements
    category_id: DIC_kwDOQ63F_c4C1hyO
    lang: ko
```

### 방문 통계 (GoatCounter)
```yaml
analytics:
  goatcounter:
    id: seungbeom
```

---

## 5. 게시물 생성 스크립트

### 파일: `scripts/generate_cs_post.py`

### 핵심 함수

| 함수 | 역할 |
|------|------|
| `get_used_topics()` | 기존 게시물에서 사용된 주제 추출 |
| `get_random_topic()` | 중복되지 않은 주제 랜덤 선택 |
| `generate_post_content()` | Groq API로 글 생성 |
| `sanitize_foreign_characters()` | 외국어 문자 필터링/제거 |
| `create_post_file()` | 마크다운 파일 저장 |

### 주제 목록 (CS_TOPICS)
- React 심화 (Fiber, Hooks, Server Components 등)
- Next.js (App Router, SSR/SSG/ISR, 캐싱 등)
- JavaScript/TypeScript 심화
- 브라우저/렌더링
- 번들러/빌드 도구
- 성능 최적화
- DevOps/CI-CD
- 클라우드/인프라
- 테스팅
- 보안

---

## 6. 관리 포인트

| 작업 | 위치 |
|------|------|
| 새 주제 추가 | `scripts/generate_cs_post.py` → `CS_TOPICS` 리스트 |
| 사이트 설정 변경 | `_config.yml` |
| 수동 게시물 작성 | `_posts/YYYY-MM-DD-제목.md` 파일 생성 |
| 워크플로우 수정 | `.github/workflows/` |
| 프로필 이미지 변경 | `assets/img/avatar.png` 교체 |

---

## 7. 외부 서비스 링크

| 서비스 | URL |
|--------|-----|
| 블로그 | https://hyunseungbeom.github.io |
| GitHub 저장소 | https://github.com/HyunSeungBeom/HyunSeungBeom.github.io |
| 방문 통계 | https://seungbeom.goatcounter.com |
| 댓글 관리 | https://github.com/HyunSeungBeom/HyunSeungBeom.github.io/discussions |
| GitHub Actions | https://github.com/HyunSeungBeom/HyunSeungBeom.github.io/actions |

---

## 8. 로컬 개발 환경

### 의존성 설치
```bash
bundle install
pip install groq
```

### 로컬 서버 실행
```bash
bundle exec jekyll serve
# http://127.0.0.1:4000 에서 확인
```

### 게시물 수동 생성 테스트
```bash
export GROQ_API_KEY="your-api-key"
python scripts/generate_cs_post.py
```

---

## 9. 게시물 작성 형식

### 파일명
```
YYYY-MM-DD-제목.md
예: 2026-01-28-react-fiber-architecture.md
```

### Front Matter
```yaml
---
title: "[Deep Dive] 제목"
date: 2026-01-28 10:00:00 +0900
categories: [카테고리]
tags: [태그1, 태그2]
---
```

---

## 10. 트러블슈팅

### 게시물이 사이트에 안 보일 때
1. `_config.yml`에 `future: true` 확인
2. 파일명 날짜 형식 확인 (YYYY-MM-DD)
3. Front Matter의 date 형식 확인

### 자동 게시물에 외국어가 포함될 때
- `sanitize_foreign_characters()` 함수에서 자동 필터링
- 새로운 패턴 발견 시 `foreign_patterns` 딕셔너리에 추가

### GitHub Actions 실패 시
1. Actions 탭에서 로그 확인
2. Secrets에 `GROQ_API_KEY` 설정 확인
