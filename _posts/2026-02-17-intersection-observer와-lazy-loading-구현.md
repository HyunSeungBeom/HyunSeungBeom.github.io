---
title: "[Deep Dive] Intersection Observer와 Lazy Loading 구현"
date: 2026-02-17 08:09:57 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Intersection Observer와 Lazy Loading은 웹 페이지의 성능을 향상시키는 기술로, 사용자가 실제로 본 콘텐츠만 로딩하여 메모리 사용량을 최적화하는 방법입니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 사용자가 웹 페이지를 접속할 때, 모든 콘텐츠를 한꺼번에 로딩하는 경우 메모리 사용량이 많아져 웹 페이지의 성능이 저하될 수 있습니다. 예를 들어, 사용자가 매우 긴 블로그 게시물의 마지막 부분만 보아도 모든 이미지와 콘텐츠를 로딩해야 하는 경우가 있습니다.
- 이전 방식의 한계: 이전에는 스크롤 이벤트를하여 사용자에게 보이는 요소를색하여 로딩하거나, 이미지를 미리 로딩한 후 필요할 때 보여주는 방식이 사용되었습니다. 하지만 이러한 방법은 복잡하고 오류가 많이 발생할 수 있습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Intersection Observer는 사용자의 화면에 요소가 보이는지의 여부를 파악하여 특정 요소를 로딩하거나 숨기는 기술입니다. 이 기술은 DOM 요소의 가시성을하고 콜백 함수를 실행합니다.
- ASCII 다이어그램으로 시각화:
```
  +---------------+
  |  사용자 화면  |
  +---------------+
           |
           |
           v
  +---------------+
  |  Intersection  |
  |  Observer      |
  +---------------+
           |
           |
           v
  +---------------+
  |  로딩 또는 숨김  |
  |  콜백 함수 실행  |
  +---------------+
```

### 코드로 이해하기
```typescript
// Intersection Observer를 생성합니다.
const observer = new IntersectionObserver((entries) => {
  // 사용자에게 보이는 요소의 경우 로딩을 시작합니다.
  if (entries[0].isIntersecting) {
    // 로딩 함수를 호출합니다.
    loadContent();
  }
}, {
  // root:null, // 기본값은 null로, 뷰포트에 대한 상대적 위치로 계산합니다.
  threshold: 1.0, // 0.0 ~ 1.0 사이의 값, 1.0이면 요소의 100%가 보일 때 콜백 함수를 호출합니다.
});

// 관찰대상 요소를 설정합니다.
const targetElement = document.getElementById('target');
observer.observe(targetElement);
```

```typescript
// 잘못된 사용 예: 잘못된 threshold 값
const observer = new IntersectionObserver((entries) => {
  // ...
}, {
  threshold: -1, // 잘못된 값, threshold는 0.0 ~ 1.0 사이의 값이어야 합니다.
});

// 올바른 사용 예: 올바른 threshold 값
const observer = new IntersectionObserver((entries) => {
  // ...
}, {
  threshold: 0.5, // 50% 이상 보일 때 콜백 함수를 호출합니다.
});
```

### 비교 분석

| 구분 | Intersection Observer | 스크롤 이벤트 | 미리 로딩 |
|------|---|---|---|
| 성능 |, 이벤트 발생 시 콜백 함수만 실행 |, 스크롤 이벤트 발생 시마다 함수를 실행 | 나쁨, 모든 콘텐츠를 일단 로딩 |
| 복잡도 | 중간, API 사용법이 이해되면 쉽게 사용 | 높은, 이벤트를하고 처리 로직을 작성해야 함 | 낮음, 이미지를 미리 로딩하는 코드만 작성하면 됨 |
| 버그 발생 가능성 | 낮음, 브라우저에서 제공하는 API | 높은, 처리 로직이 복잡 | 낮음, 단순한 로직 |

### 실전 팁
- Best Practice: Intersection Observer를 사용하여 콘텐츠의 로딩을 지연시키는 것을 Lazy Loading이라고 부릅니다. 따라서 사용자에게 최적의 경험을 제공하는 웹 페이지를 만들기 위해서는 Lazy Loading을 적극 활용하는 것이 좋습니다.
- 흔한 실수와 해결법: 잘못된 threshold 값으로 인한 오작동, 관찰대상 요소가 변경되었지만 관찰을 중단하지 않은 경우 등이 있습니다. 해결하려면 threshold 값을 올바르게 설정하고, 요소가 변경될 때 관찰을 중단하는 코드를 추가해야 합니다.
- 성능 관련 주의사항: Intersection Observer를 사용할 때는 threshold 값을 조절하여 사용자에게 최적의 경험을 제공하는 것을 목표로 해야 합니다. 또한, 관찰 대상 요소가 너무 많다면 성능이 저하될 수 있으므로 주의가 필요합니다.

### 한 줄 정리
Intersection Observer와 Lazy Loading은 웹 페이지의 성능을 향상시키는 기술로, 사용자가 실제로 본 콘텐츠만 로딩하여 메모리 사용량을 최적화하는 방법입니다.