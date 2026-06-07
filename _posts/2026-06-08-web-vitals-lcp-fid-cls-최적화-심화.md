---
title: "[Deep Dive] Web Vitals (LCP, FID, CLS) 최적화 심화"
date: 2026-06-08 08:26:46 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Vitals 최적화는 웹 페이지의 성능을 하고 개선하기 위한 표준화된 지표로, LCP, FID, CLS를 포함한다.

## Deep Dive

### 왜 필요한가?
- Web Vitals은 웹 페이지의 로딩 속도, 상호작용성,적 안정성을 측정하여 사용자 경험이 개선될 수 있도록 도와준다.
- 이전 방식의 한계는 사용자 경험이나 성능을 측정하는 표준화된 방법이 없다는 점이었다.

### 내부 동작 원리
- Web Vitals의 핵심 메커니즘은 사용자의 브라우저와 서버 간의 상호작용을 측정하여 지표를 계산하는 것이다.
- LCP(Largest Contentful Paint)는 가장 큰 콘텐츠 요소가 화면에 표시되는 시간을 측정한다.
- FID(First Input Delay)는 사용자가 상호작용을 시작할 때까지의 시간을 측정한다.
- CLS(Cumulative Layout Shift)는 레이아웃의 이동을 측정하여 사용자 경험이 영향을 받는지 판단한다.
 
```
  +---------------+
  |  사용자 요청  |
  +---------------+
           |
           |
           v
  +---------------+
  |  브라우저 렌더링  |
  |  (LCP, FID, CLS)  |
  +---------------+
           |
           |
           v
  +---------------+
  |  성능 측정 결과  |
  |  (Web Vitals)    |
  +---------------+
```

### 코드로 이해하기

```typescript
// LCP 측정을 위한 코드 예제
function calculateLCP() {
  const performance = window.performance;
  const largestContentfulPaint = performance.getEntriesByType('largest-contentful-paint')[0];
  return largestContentfulPaint.renderTime;
}
```

```typescript
// 올바른 사용 예: LCP를 개선하기 위한 이미지 캐싱
const imageCache = {};
function loadImage(url) {
  if (imageCache[url]) {
    return imageCache[url];
  }
  const img = new Image();
  img.src = url;
  imageCache[url] = img;
  return img;
}
```

### 비교 분석

| 지표 | LCP | FID | CLS |
|------|-----|-----|-----|
| 측정대상 | 콘텐츠 로딩 | 상호작용 | 레이아웃 이동 |
| 목적 | 로딩 속도 개선 | 사용자 경험이 개선 |적 안정성 |
| 좋음/나쁨 | 빠를수록 좋음 | 짧을수록 좋음 | 낮을수록 좋음 |

### 실전 팁
- Best Practice: 캐싱, 최적화, 콘텐츠 분할을 통해 로딩 속도를 개선한다.
- 흔한 실수: 불필요한 스크립트 로딩, 큰 이미지 사용 등이 성능을 저하시킨다.
- 성능 관련 주의사항: 모바일 사용자의 경우 성능이 더 중요하므로 최적화를 신중히 수행해야한다.

### 한 줄 정리
Web Vitals은 웹 페이지의 성능을 측정하고 개선하기 위한 표준화된 지표로, LCP, FID, CLS를 포함하여 사용자 경험이 개선되도록 도와준다.