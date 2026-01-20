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
당신은 시니어 프론트엔드 개발자이자 DevOps 전문가입니다. 다음 주제에 대해 심화 기술 블로그 포스트를 작성해주세요.

주제: {topic}

다음 형식으로 깊이있게 작성해주세요:

## TL;DR
- 바쁜 독자를 위한 핵심 한 줄 요약

## 선행 지식
- 이 글을 이해하기 위해 알아야 할 개념들
- (필수 선행 지식이 없으면 "특별한 선행 지식이 필요하지 않습니다" 라고 작성)

## 탄생 배경
- 이 기술/개념이 왜 생겼는가?
- 이전에는 어떤 문제가 있었는가?
- 어떤 한계를 극복하기 위해 등장했는가?

## 역사와 발전 과정
- 언제, 누가, 어떤 맥락에서 만들었는지
- 주요 변화와 발전 흐름
- 현재 상태

## 개념 정의
- 정확히 무엇인가?
- 핵심 용어 정리

## 동작 원리
- 내부적으로 어떻게 작동하는가?
- 다이어그램, 표, 또는 ASCII art로 시각화
- 코드 레벨에서의 구현 예제

## 실무 활용
- 실제 프로젝트에서 어떻게 쓰이는가?
- 구체적인 코드 예제 (TypeScript/JavaScript/React 등)
- Best Practice

## 비교 분석
- 비슷한 개념/기술과의 차이점
- 각각 언제 써야 하는가?
- 트레이드오프 분석 (표로 정리)

## 한계와 주의점
- 이 기술의 단점
- 흔히 하는 실수
- 안티패턴

## 미래 전망
- 앞으로의 발전 방향
- 관련 기술 동향

## 정리
- 핵심 포인트 3~5줄 요약
- 한 문장 결론

작성 규칙:
- 한국어로 작성
- 마크다운 형식 사용
- 코드 블록은 적절한 언어 태그 사용 (typescript, javascript, tsx, bash 등)
- 이모지 사용하지 않음
- 전체 길이는 2000~3000자 정도로 깊이있게
- 단순한 설명이 아닌 "왜?"에 초점
- 면접 관련 내용은 포함하지 않음
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
