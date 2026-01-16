#!/usr/bin/env python3
"""
매일 CS 지식 포스트를 자동 생성하는 스크립트
Gemini API를 사용하여 랜덤 CS 주제에 대한 글을 생성합니다.
"""

import os
import random
from datetime import datetime
import google.generativeai as genai

# CS 주제 목록 (난이도: 쉬움, 중간, 어려움)
CS_TOPICS = {
    "easy": [
        "변수와 자료형",
        "조건문과 반복문",
        "배열과 리스트의 차이",
        "함수란 무엇인가",
        "객체지향 프로그래밍 기초",
        "HTTP와 HTTPS의 차이",
        "쿠키와 세션",
        "GET과 POST의 차이",
        "JSON이란",
        "API란 무엇인가",
        "Git 기본 명령어",
        "프론트엔드와 백엔드",
        "데이터베이스란",
        "SQL 기본 문법",
        "클라이언트와 서버",
    ],
    "medium": [
        "TCP와 UDP의 차이",
        "프로세스와 스레드",
        "스택과 큐 자료구조",
        "해시 테이블 원리",
        "이진 탐색 알고리즘",
        "시간복잡도 Big-O 표기법",
        "REST API 설계 원칙",
        "데이터베이스 인덱스",
        "정규화와 비정규화",
        "캐시의 원리",
        "동기와 비동기 처리",
        "SOLID 원칙",
        "디자인 패턴 - 싱글톤",
        "디자인 패턴 - 팩토리",
        "OAuth 인증 방식",
    ],
    "hard": [
        "운영체제 스케줄링 알고리즘",
        "가상 메모리와 페이징",
        "데드락과 해결 방법",
        "트랜잭션 격리 수준",
        "CAP 정리",
        "분산 시스템의 일관성",
        "마이크로서비스 아키텍처",
        "메시지 큐와 이벤트 드리븐",
        "Docker 컨테이너 원리",
        "Kubernetes 기본 개념",
        "CI/CD 파이프라인",
        "로드 밸런싱 전략",
        "데이터베이스 샤딩",
        "동시성 제어와 락",
        "가비지 컬렉션 원리",
    ]
}

def get_random_topic():
    """난이도를 랜덤으로 선택하고 해당 난이도에서 주제 선택"""
    difficulty = random.choice(["easy", "medium", "hard"])
    topic = random.choice(CS_TOPICS[difficulty])
    return topic, difficulty

def generate_post_content(topic: str, difficulty: str) -> str:
    """Gemini API를 사용하여 포스트 내용 생성"""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    difficulty_kr = {"easy": "쉬움", "medium": "중간", "hard": "어려움"}[difficulty]

    prompt = f"""
당신은 친절한 CS 교육자입니다. 다음 주제에 대해 블로그 포스트를 작성해주세요.

주제: {topic}
난이도: {difficulty_kr}

다음 형식으로 작성해주세요:
1. 핵심 개념을 쉽게 설명 (비유 사용 권장)
2. 실제 사용 예시나 코드 예제
3. 면접에서 자주 나오는 질문과 답변
4. 한 줄 요약

작성 규칙:
- 한국어로 작성
- 마크다운 형식 사용
- 코드 블록은 적절한 언어 태그 사용
- 이모지는 최소한으로 사용
- 전체 길이는 800~1200자 정도
"""

    response = model.generate_content(prompt)
    return response.text

def create_post_file(topic: str, difficulty: str, content: str):
    """마크다운 포스트 파일 생성"""

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    time_str = today.strftime("%Y-%m-%d %H:%M:%S +0900")

    # 파일명용 슬러그 생성
    slug = topic.replace(" ", "-").replace("/", "-").lower()
    filename = f"{date_str}-{slug}.md"

    difficulty_tag = {"easy": "기초", "medium": "중급", "hard": "심화"}[difficulty]

    front_matter = f"""---
title: "[CS 지식] {topic}"
date: {time_str}
categories: [개발뉴스]
tags: [CS, {difficulty_tag}]
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
    print("CS 지식 포스트 생성 시작...")

    # 랜덤 주제 선택
    topic, difficulty = get_random_topic()
    print(f"선택된 주제: {topic} (난이도: {difficulty})")

    # Gemini로 내용 생성
    content = generate_post_content(topic, difficulty)

    # 파일 생성
    filename = create_post_file(topic, difficulty, content)

    print("완료!")
    return filename

if __name__ == "__main__":
    main()
