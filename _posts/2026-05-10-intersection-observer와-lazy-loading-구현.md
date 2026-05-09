---
title: "[Deep Dive] Intersection Observer와 Lazy Loading 구현"
date: 2026-05-10 08:19:33 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Intersection Observer와 Lazy Loading 구현은 사용자에게 더 나은 사용자 경험을 제공하기 위해 웹 페이지의 성능을 최적화하는 중요한 기술입니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 웹 페이지의 성능을 최적화하여 사용자에게 더 빠르고 효율적인 사용자 경험을 제공합니다.
- 이전 방식의 한계: 이전에는 일반적으로 전체 페이지를 로딩하고 사용자에게 보여주는 방식을 사용했습니다. 하지만 이러한 방식은 페이지 로딩 시간이 길어지고 사용자 경험을 나쁘게 만들었습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Intersection Observer는 웹 페이지의 특정 요소가 사용자 화면에 보이는지 관찰하고, 사용자 화면에 보일 때 특정 동작을 수행하도록 설정할 수 있습니다. Lazy Loading은 필요한 리소스를 미리 로딩하여 사용자에게 더 빠른 사용자 경험을 제공합니다.
- ASCII 다이어그램으로 시각화:
```
  +---------------+
  |  웹 페이지   |
  +---------------+
           |
           |
           v
  +---------------+
  | Intersection  |
  |  Observer     |
  +---------------+
           |
           |
           v
  +---------------+
  |  Lazy Loading  |
  +---------------+
           |
           |
           v
  +---------------+
  |  사용자 화면  |
  +---------------+
```

### 코드로 이해하기
```typescript
// Intersection Observer 예제
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    console.log('요소가 사용자 화면에 보입니다.');
  } else {
    console.log('요소가 사용자 화면에서 사라졌습니다.');
  }
}, {
  threshold: 1.0,
});

const target = document.querySelector('#target');
observer.observe(target);
```

```typescript
// 잘못된 사용 예
// 올바른 사용 예
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    // 리소스를 로딩합니다.
    const img = new Image();
    img.src = 'image.jpg';
    document.querySelector('#target').appendChild(img);
  }
}, {
  threshold: 1.0,
});
```

### 비교 분석

| 구분 | Intersection Observer | Lazy Loading |
|------|---|---|
| 목적 | 사용자 화면에 보이는 요소 관찰 | 필요한 리소스를 미리 로딩 |
| 동작 원리 | 사용자 화면에 보이는 요소를 관찰하여 동작 | 필요한 리소스를 미리 로딩하여 사용자에게 더 빠른 사용자 경험 제공 |
| 활용 예 | 이미지 로딩, 사용자 행동 분석 | 이미지 로딩, 동영상 로딩 |

### 실전 팁
- Best Practice: Intersection Observer와 Lazy Loading을 함께 사용하여 사용자에게 더 나은 사용자 경험을 제공합니다.
- 흔한 실수와 해결법: Intersection Observer에서 threshold 값을 잘못 설정하여 사용자 화면에 보이는 요소를 정확하게 관찰하지 못하는 경우가 있습니다. threshold 값을 조정하여 사용자 화면에 보이는 요소를 정확하게 관찰합니다.
- 성능 관련 주의사항: Intersection Observer와 Lazy Loading을 사용할 때 리소스를 과도하게 로딩하여 성능이 저하되는 경우가 있습니다. 리소스를 적절하게 로딩하여 성능을 최적화합니다.

### 한 줄 정리
Intersection Observer와 Lazy Loading은 사용자에게 더 나은 사용자 경험을 제공하기 위해 웹 페이지의 성능을 최적화하는 중요한 기술입니다.