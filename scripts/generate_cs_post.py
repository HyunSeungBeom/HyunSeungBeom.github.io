#!/usr/bin/env python3
"""
매일 CS 지식 포스트를 자동 생성하는 스크립트
Groq API를 사용하여 랜덤 CS 주제에 대한 글을 생성합니다.
"""

import os
import random
from datetime import datetime
from groq import Groq

# 프론트엔드 & DevOps 심화 주제 목록
CS_TOPICS = [
    # React 심화
    "React Fiber Architecture와 Reconciliation 알고리즘",
    "React 동시성 모드 (Concurrent Mode)와 Suspense 내부 동작",
    "Virtual DOM Diffing 알고리즘과 Key의 중요성",
    "React Hooks의 내부 구현 원리 (Linked List와 호출 순서)",
    "React Server Components vs Client Components 아키텍처",
    "useEffect vs useLayoutEffect 실행 타이밍과 브라우저 렌더링",
    "React.memo, useMemo, useCallback 최적화 전략과 함정",
    "React 상태 관리 라이브러리 비교 (Redux, Zustand, Jotai, Recoil)",

    # Next.js 심화
    "Next.js App Router vs Pages Router 아키텍처 차이",
    "Next.js SSR, SSG, ISR, PPR 렌더링 전략 비교",
    "Next.js 서버 액션과 데이터 페칭 패턴",
    "Next.js 캐싱 전략 (Request Memoization, Data Cache, Full Route Cache)",
    "Next.js Middleware와 Edge Runtime 활용",
    "Next.js 이미지 최적화와 Layout Shift 방지",

    # JavaScript/TypeScript 심화
    "JavaScript 이벤트 루프와 마이크로태스크 큐",
    "JavaScript 클로저와 메모리 누수 패턴",
    "JavaScript Prototype Chain과 상속 메커니즘",
    "JavaScript 엔진 최적화 (V8 Hidden Class, Inline Caching)",
    "TypeScript 타입 시스템 심화 (Conditional Types, Mapped Types, Template Literal Types)",
    "TypeScript 컴파일러 동작 원리와 Declaration Files",
    "WeakMap, WeakSet과 가비지 컬렉션",
    "JavaScript Module System 비교 (CommonJS, ESM, AMD, UMD)",

    # 브라우저/렌더링
    "브라우저 렌더링 파이프라인 (DOM, CSSOM, Render Tree, Layout, Paint, Composite)",
    "Critical Rendering Path 최적화 전략",
    "Reflow vs Repaint와 성능 최적화",
    "브라우저 캐싱 전략 (Memory Cache, Disk Cache, Service Worker Cache)",
    "Web Vitals (LCP, FID, CLS) 최적화 심화",
    "requestAnimationFrame vs setTimeout 차이와 애니메이션 최적화",
    "Intersection Observer와 Lazy Loading 구현",
    "Web Worker와 멀티스레딩 패턴",

    # 번들러/빌드 도구
    "Webpack vs Vite vs Turbopack 번들링 전략 비교",
    "Tree Shaking 동작 원리와 Side Effects",
    "Code Splitting과 Dynamic Import 최적화",
    "Module Federation과 마이크로 프론트엔드",
    "Source Map 동작 원리와 디버깅",
    "Babel vs SWC vs esbuild 트랜스파일러 비교",

    # 성능 최적화
    "프론트엔드 성능 측정과 Lighthouse 점수 최적화",
    "이미지 최적화 전략 (WebP, AVIF, Lazy Loading, Responsive Images)",
    "폰트 최적화와 FOIT, FOUT 해결",
    "JavaScript 번들 사이즈 최적화 전략",
    "Prefetch, Preload, Preconnect 리소스 힌트 활용",
    "메모리 누수 탐지와 Chrome DevTools 프로파일링",

    # DevOps/CI-CD
    "Docker 컨테이너 원리와 이미지 레이어 최적화",
    "Kubernetes 아키텍처와 Pod 스케줄링",
    "GitHub Actions 워크플로우 최적화와 캐싱 전략",
    "CI/CD 파이프라인 설계 패턴",
    "Blue-Green vs Canary vs Rolling 배포 전략",
    "Infrastructure as Code (Terraform, Pulumi)",
    "모니터링과 Observability (Prometheus, Grafana, Datadog)",
    "로그 수집과 분석 (ELK Stack, Loki)",

    # 클라우드/인프라
    "AWS S3 + CloudFront 정적 웹 호스팅 최적화",
    "Vercel vs Netlify vs AWS Amplify 플랫폼 비교",
    "Edge Computing과 Edge Functions 활용",
    "CDN 동작 원리와 캐시 무효화 전략",
    "서버리스 아키텍처와 Cold Start 최적화",
    "AWS Lambda@Edge vs CloudFlare Workers",

    # 테스팅
    "프론트엔드 테스트 전략 (Unit, Integration, E2E)",
    "Testing Library 철학과 접근성 기반 테스트",
    "Playwright vs Cypress E2E 테스트 비교",
    "Visual Regression Testing 구축",
    "MSW(Mock Service Worker)를 활용한 API Mocking",

    # 보안
    "프론트엔드 보안 취약점 (XSS, CSRF, Clickjacking)",
    "Content Security Policy (CSP) 설정과 활용",
    "CORS 동작 원리와 Preflight Request",
    "JWT vs Session 인증 방식 비교",
    "OAuth 2.0 / OpenID Connect 플로우",
]

def get_random_topic():
    """랜덤 주제 선택"""
    topic = random.choice(CS_TOPICS)
    return topic

def generate_post_content(topic: str) -> str:
    """Groq API를 사용하여 포스트 내용 생성"""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY 환경변수가 설정되지 않았습니다.")

    client = Groq(api_key=api_key)

    prompt = f"""
당신은 시니어 프론트엔드 개발자이자 DevOps 전문가입니다. 다음 주제에 대해 Deep Dive 기술 블로그 포스트를 작성해주세요.

주제: {topic}

다음 형식으로 작성해주세요:

---

## 표면적 이해
(한 줄로 간단히 설명)

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제
- 이전 방식의 한계

### 내부 동작 원리
- 핵심 메커니즘 설명
- ASCII 다이어그램으로 시각화 (필수)

```
(여기에 ASCII 다이어그램)
```

### 코드로 이해하기

```typescript
// 실제 동작을 보여주는 코드 예제
```

```typescript
// 잘못된 사용 예 (❌)
// 올바른 사용 예 (✅)
```

### 비교 분석

| 구분 | A | B | C |
|------|---|---|---|
| 특성1 | | | |
| 특성2 | | | |

### 실전 팁
- Best Practice
- 흔한 실수와 해결법
- 성능 관련 주의사항

### 한 줄 정리
(핵심을 한 문장으로)

---

작성 규칙:
- 반드시 한국어로만 작성 (중국어, 일본어, 영어 문장 절대 금지)
- 기술 용어는 영어 그대로 사용 가능 (예: Virtual DOM, Reconciliation)
- 마크다운 형식 사용
- 코드 블록은 적절한 언어 태그 사용 (typescript, javascript, tsx, bash 등)
- 이모지 사용하지 않음
- ASCII 다이어그램 필수 포함
- 표(table)로 비교 분석 필수 포함
- 전체 길이는 2500~3500자 정도로 깊이있게
- 단순한 정의 나열이 아닌 "왜?"와 "어떻게?"에 초점
- 면접 준비, 면접 팁 등의 내용은 포함하지 않음
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

def create_post_file(topic: str, content: str):
    """마크다운 포스트 파일 생성"""

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%Y-%m-%d %H:%M:%S +0900")

    # 파일명용 슬러그 생성
    slug = topic.replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "").replace(",", "").lower()
    # 슬러그 길이 제한
    slug = slug[:50]
    filename = f"{date_str}-{slug}.md"

    front_matter = f"""---
title: "[Deep Dive] {topic}"
date: {time_str}
categories: [개발뉴스]
tags: [CS, 심화]
---

"""

    full_content = front_matter + content

    # _posts 폴더에 저장
    posts_dir = os.path.join(os.path.dirname(__file__), "..", "_posts")
    os.makedirs(posts_dir, exist_ok=True)

    filepath = os.path.join(posts_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"포스트 생성 완료: {filename}")
    return filename

def main():
    print("CS Deep Dive 포스트 생성 시작...")

    # 랜덤 주제 선택
    topic = get_random_topic()
    print(f"선택된 주제: {topic}")

    # Groq로 내용 생성
    content = generate_post_content(topic)

    # 파일 생성
    filename = create_post_file(topic, content)

    print("완료!")
    return filename

if __name__ == "__main__":
    main()
