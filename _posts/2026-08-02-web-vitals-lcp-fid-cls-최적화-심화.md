---
title: "[Deep Dive] Web Vitals (LCP, FID, CLS) 최적화 심화"
date: 2026-08-02 08:57:27 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Vitals은 사용자 경험을 평가하는 데 사용되는 메트릭이며, LCP, FID, CLS를 최적화하여 사용자 경험을 개선하는 것을 목표로 한다.

## Deep Dive

### 왜 필요한가?
Web Vitals은 사용자 경험을 평가하는 데 사용되는 메트릭이며, LCP(Largest Contentful Paint), FID(First Input Delay), CLS(Cumulative Layout Shift) 등이 포함된다. 이전 방식의 한계는 사용자 경험을 정확하게 측정하지 못한다는 점이었다. Web Vitals은 이러한 한계를 극복하여 사용자 경험을 더 정확하게 평가할 수 있다.

### 내부 동작 원리
LCP는 페이지에서 가장 큰 콘텐츠 요소가 렌더링되는 시간을 측정하며, FID는 사용자가 페이지와 상호작용할 수 있는 시간을 측정한다. CLS는 레이아웃이 변경될 때 발생하는 시각적 불안정성을 측정한다. 다음은 내부 동작 원리를 나타내는 ASCII 다이어그램이다.
```
                      +---------------+
                      |  페이지 로드  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  LCP 측정    |
                      |  (최대 콘텐츠  |
                      |   요소 렌더링) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  FID 측정    |
                      |  (사용자 상호작용  |
                      |   가능 시간)     |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  CLS 측정    |
                      |  (레이아웃 불안정성) |
                      +---------------+
```

### 코드로 이해하기
다음은 Web Vitals를 측정하는 예제 코드이다.
```typescript
import { getLCP, getFID, getCLS } from 'web-vitals';

// LCP 측정
getLCP().then((metric) => {
  console.log('LCP:', metric);
});

// FID 측정
getFID().then((metric) => {
  console.log('FID:', metric);
});

// CLS 측정
getCLS().then((metric) => {
  console.log('CLS:', metric);
});
```

```typescript
// 잘못된 사용 예: Web Vitals를 mesure하지 않는다.
console.log('LCP:', 0);
console.log('FID:', 0);
console.log('CLS:', 0);

// 올바른 사용 예: Web Vitals를 측정한다.
import { getLCP, getFID, getCLS } from 'web-vitals';
getLCP().then((metric) => {
  console.log('LCP:', metric);
});
getFID().then((metric) => {
  console.log('FID:', metric);
});
getCLS().then((metric) => {
  console.log('CLS:', metric);
});
```

### 비교 분석
다음은 Web Vitals 메트릭을 비교 분석하는 표이다.
| 구분 | LCP | FID | CLS |
|------|-----|-----|-----|
| 측정 항목 | 최대 콘텐츠 요소 렌더링 시간 | 사용자 상호작용 가능 시간 | 레이아웃 불안정성 |
| 목표 값 | 2.5초 이내 | 100ms 이내 | 0.1 이내 |
| 영향 | 사용자 경험, 검색 엔진 최적화 | 사용자 경험, 검색 엔진 최적화 | 사용자 경험 |

### 실전 팁
- Web Vitals를 측정하여 사용자 경험을 개선한다.
- LCP를 개선하기 위해 이미지 최적화, 코드 분할, 캐싱을 사용한다.
- FID를 개선하기 위해 코드 최적화, 캐싱, Lazy Loading등을 사용한다.
- CLS를 개선하기 위해 레이아웃 최적화, 이미지 최적화, 애니메이션 최적화등을 사용한다.

### 한 줄 정리
Web Vitals을 최적화하여 사용자 경험을 개선하는 것은 검색 엔진 최적화와 사용자도를 향상시키는 데 중요하다.