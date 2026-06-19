---
title: "[Deep Dive] Web Vitals (LCP, FID, CLS) 최적화 심화"
date: 2026-06-20 08:26:00 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Vitals는 웹 사이트의 사용자 경험을 평가하고 최적화하는 데 도움이 되는 일련의 지표로, LCP(Largest Contentful Paint), FID(First Input Delay), CLS(Cumulative Layout Shift)로 구성됩니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 웹 사이트의 로딩 속도, 사용자 상호작용, 레이아웃 안정성을 평가하고 최적화하는 것
- 이전 방식의 한계: 이전에는 웹 사이트의 성능을 평가하기 위해 여러 지표를 사용했지만, 사용자 경험에 대한 전체적인 이해를 제공하지 못했습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Web Vitals는 브라우저에서 제공하는 API를 사용하여 웹 사이트의 성능을 평가합니다. LCP는 가장 큰 콘텐츠 요소의 페인트 을 측정하며, FID는 사용자와의 첫 상호작용에 대한 지연 시간을 측정합니다. CLS는 웹 페이지의 레이아웃이 얼마나 자주 변경되는지 측정합니다.
- ASCII 다이어그램으로 시각화:
```
                          +---------------+
                          |  브라우저   |
                          +---------------+
                                    |
                                    |
                                    v
                          +---------------+
                          |  Web Vitals  |
                          |  (LCP, FID, CLS) |
                          +---------------+
                                    |
                                    |
                                    v
                          +---------------+
                          |  성능 평가  |
                          +---------------+
                                    |
                                    |
                                    v
                          +---------------+
                          |  최적화   |
                          +---------------+
```

### 코드로 이해하기
```typescript
// LCP 예제
function measureLCP() {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const largestPaint = entries.reduce((max, entry) => {
      return entry.size > max.size ? entry : max;
    }, { size: 0 });
    console.log('LCP:', largestPaint);
  });
  observer.observe({ entryTypes: ['paint'] });
}

// FID 예제
function measureFID() {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const firstInput = entries.find((entry) => entry.entryType === 'first-input');
    console.log('FID:', firstInput);
  });
  observer.observe({ entryTypes: ['first-input'] });
}

// CLS 예제
function measureCLS() {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const layoutShifts = entries.filter((entry) => entry.entryType === 'layout-shift');
    console.log('CLS:', layoutShifts);
  });
  observer.observe({ entryTypes: ['layout-shift'] });
}
```

```typescript
// 잘못된 사용 예: 웹 사이트의 모든 요소를 LCP로 측정하는 경우
function measureLCPWrong() {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    console.log('LCP:', entries);
  });
  observer.observe({ entryTypes: ['paint'] });
}

// 올바른 사용 예: 가장 큰 콘텐츠 요소만 LCP로 측정하는 경우
function measureLCPRight() {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const largestPaint = entries.reduce((max, entry) => {
      return entry.size > max.size ? entry : max;
    }, { size: 0 });
    console.log('LCP:', largestPaint);
  });
  observer.observe({ entryTypes: ['paint'] });
}
```

### 비교 분석
| 구분 | LCP | FID | CLS |
|------|---|---|---|
| 측정 대상 | 가장 큰 콘텐츠 요소 | 첫 상호작용 | 레이아웃 임 |
|정 방법 | 브라우저의 페인트 이벤트 | 브라우저의 첫 입력 이벤트 | 브라우저의 레이아웃 변경 이벤트 |
| 최적화 방법 | 이미지, 비디오, 스크립트 파일 크기 축소 | 사용자 상호작용에 대한 지연 시간 단축 | 레이아웃 변경 최소화 |

### 실전 팁
- Best Practice: Web Vitals 지표를 사용하여 웹 사이트의 성능을 평가하고 최적화하기
- 흔한 실수와 해결법: 잘못된 측정 대상이나 방법을 사용하는 경우, 올바른 측정 방법을 사용하도록 수정해야 합니다.
- 성능 관련 주의사항: 웹 사이트의 성능을 개선하는 동안 사용자 경험을 저하하지 않도록 주의해야 합니다.

### 한 줄 정리
Web Vitals는 웹 사이트의 사용자 경험을 평가하고 최적화하는 데 도움이 되는 일련의 지표입니다.