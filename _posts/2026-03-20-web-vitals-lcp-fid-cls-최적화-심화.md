---
title: "[Deep Dive] Web Vitals (LCP, FID, CLS) 최적화 심화"
date: 2026-03-20 08:10:13 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Vitals 최적화는 웹 페이지의 성능을 개하는 기술입니다.

## Deep Dive

### 왜 필요한가?
- Web Vitals은 웹 페이지의 성능 지표를 측정하고 개선하는 기술입니다. 주로 LCP, FID, CLS를 측정하여 사용자 경험을 향상시킵니다.
- 이전 방식은 페이지 로드 시간이나 서버 응답 시간만 측정하였지만, Web Vitals은 사용자 인터랙션 및 시각적 안정성을 포함하여 더욱한 성능 측정을 제공합니다.

### 내부 동작 원리
- Web Vitals은 사용자 인터랙션 및 시각적 안정성을 측정합니다. LCP(Largest Contentful Paint)는 가장 큰 콘텐츠 요소의 표시 시간을 측정하며, FID(First Input Delay)는 사용자 입력에 대한 초기 반응 시간을 측정합니다. CLS(Cumulative Layout Shift)는 레이아웃의 변화로 인한 안정성을 측정합니다.
```
                              +---------------+
                              |  사용자 입력  |
                              +---------------+
                                    |
                                    |
                                    v
                              +---------------+
                              |  브라우저 렌더링  |
                              +---------------+
                                    |
                                    |
                                    v
                              +---------------+
                              |  LCP, FID, CLS  |
                              |  measurement    |
                              +---------------+
                                    |
                                    |
                                    v
                              +---------------+
                              |  성능 지표 분석  |
                              +---------------+
```

### 코드로 이해하기
```typescript
// Web Vitals measurement 예제
function measureWebVitals() {
  // LCP 측정
  const lcp = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const lcpEntry = entries.find((entry) => entry.name === 'largest-contentful-paint');
    if (lcpEntry) {
      console.log('LCP:', lcpEntry.startTime);
    }
  });
  lcp.observe({ entryTypes: ['largest-contentful-paint'] });

  // FID 측정
  const fid = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const fidEntry = entries.find((entry) => entry.name === 'first-input');
    if (fidEntry) {
      console.log('FID:', fidEntry.processingStart - fidEntry.startTime);
    }
  });
  fid.observe({ entryTypes: ['first-input'] });

  // CLS 측정
  const cls = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const clsEntry = entries.find((entry) => entry.name === 'layout-shift');
    if (clsEntry) {
      console.log('CLS:', clsEntry.value);
    }
  });
  cls.observe({ entryTypes: ['layout-shift'] });
}
```

```typescript
// 잘못된 사용 예: measurement를 호출하지 않음
function wrongExample() {
  // measurement 코드 작성이 필요함
}

// 올바른 사용 예: measurement 호출
function correctExample() {
  measureWebVitals();
}
```

### 비교 분석

| 성능 지표 | 설명 | 중요도 |
|------|---|---|
| LCP | 가장 큰 콘텐츠 요소의 표시 시간 | 높 음 |
| FID | 사용자 입력에 대한 초기 반응 시간 | 높 음 |
| CLS | 레이아웃의 변화로 인한 안정성 | 중 등 |

### 실전 팁
- 캐싱, 압축, 미니파이 등 최적화 기법을 적용하여 페이지 로드 시간을 줄여야 합니다.
- 사용자 인터랙션에 대한 초기 반응 시간을 줄이기 위해 FID 최적화를 수행해야 합니다.
- 레이아웃의 변화로 인한 안정성을 높이기 위해 CLS 최적화를 수행해야 합니다.
- 성능 지표를 정기적으로 모니터링하여 최적화의를 확인해야 합니다.

### 한 줄 정리
웹 페이지의 성능을 개선하기 위해 Web Vitals을 사용하여 LCP, FID, CLS를 측정하고 최적화하여 사용자 경험을 향상시킵니다.