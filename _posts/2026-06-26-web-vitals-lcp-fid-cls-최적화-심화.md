---
title: "[Deep Dive] Web Vitals (LCP, FID, CLS) 최적화 심화"
date: 2026-06-26 08:31:35 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Vitals(LCP, FID, CLS) 최적화 심화는 웹 페이지의 성능을 최적화하고 사용자 경험을 개선하는 방법에 대한 심화적인 이해를 제공합니다.

## Deep Dive

### 왜 필요한가?
Web Vitals(LCP, FID, CLS) 최적화가 필요한 이유는 웹 페이지의 성능과 사용자 경험을 개선하기 위해서입니다. 이전에는 페이지 로딩 속도나 렌더링 시간만을 고려하였지만, 이제는 사용자와의 상호작용을 포함한 전체적인 사용자 경험을 평가하고 개선하는 것이 중요해졌습니다. LCP(Largest Contentful Paint)와 FID(First Input Delay), CLS(Cumulative Layout Shift)와 같은 지표들이 웹 페이지의 성능과 사용자 경험을 측정하는 데 중요한 역할을 합니다.

### 내부 동작 원리
Web Vitals의 내부 동작 원리는 다음과 같이 설명할 수 있습니다.
```
                      +-------------------+
                      |  사용자 요청   |
                      +-------------------+
                             |
                             |
                             v
                      +-------------------+
                      |  페이지 로딩   |
                      +-------------------+
                             |
                             |
                             v
                      +-------------------+
                      |  LCP 계산      |
                      |  (최대 콘텐츠 출력) |
                      +-------------------+
                             |
                             |
                             v
                      +-------------------+
                      |  FID 계산      |
                      |  (첫 번째 입력 지연) |
                      +-------------------+
                             |
                             |
                             v
                      +-------------------+
                      |  CLS 계산      |
                      |  (누적 레이아웃 변동) |
                      +-------------------+
                             |
                             |
                             v
                      +-------------------+
                      |  성능 보고      |
                      |  (Web Vitals 지표) |
                      +-------------------+
```
이 다이어그램은 사용자 요청에서부터 페이지 로딩, LCP, FID, CLS 계산, 성능 보고까지의 일련의 과정을 보여줍니다.

### 코드로 이해하기
예를 들어, 다음 코드는 Web Vitals를 측정하는 방법을 보여줍니다.
```typescript
// LCP 측정
function measureLCP() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lcpEntry = entries.find((entry) => entry.entryType === 'largest-contentful-paint');
    if (lcpEntry) {
      console.log('LCP:', lcpEntry.duration);
    }
  });
  observer.observe({ entryTypes: ['largest-contentful-paint'] });
}

// FID 측정
function measureFID() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const fidEntry = entries.find((entry) => entry.entryType === 'first-input');
    if (fidEntry) {
      console.log('FID:', fidEntry.duration);
    }
  });
  observer.observe({ entryTypes: ['first-input'] });
}

// CLS 측정
function measureCLS() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const clsEntry = entries.find((entry) => entry.entryType === 'layout-shift');
    if (clsEntry) {
      console.log('CLS:', clsEntry.value);
    }
  });
  observer.observe({ entryTypes: ['layout-shift'] });
}
```
다음은 잘못된 사용 예와 올바른 사용 예입니다.
```typescript
// 잘못된 사용 예
function measureLCPWrong() {
  const observer = new PerformanceObserver((list) => {
    console.log('LCP:', list.getEntries());
  });
  observer.observe({ entryTypes: ['largest-contentful-paint'] });
}

// 올바른 사용 예
function measureLCPCorrect() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lcpEntry = entries.find((entry) => entry.entryType === 'largest-contentful-paint');
    if (lcpEntry) {
      console.log('LCP:', lcpEntry.duration);
    }
  });
  observer.observe({ entryTypes: ['largest-contentful-paint'] });
}
```

### 비교 분석
다음 표는 Web Vitals의 세 가지 지표(LCP, FID, CLS)를 비교 분석합니다.
| 구분 | LCP | FID | CLS |
|------|---|---|---|
| 측정 대상 | 최대 콘텐츠 출력 | 첫 번째 입력 지연 | 누적 레이아웃 변동 |
| 측정 방법 | PerformanceObserver | PerformanceObserver | PerformanceObserver |
| 최적화 목표 | 페이지 로딩 속도 개선 | 입력 응답 시간 개선 | 레이아웃 안정성 개선 |

### 실전 팁
Web Vitals를 최적화하는 데에는 다음과 같은 실전 팁이 있습니다.
* Best Practice: 페이지의 콘텐츠를 가능한 한 빠르게 로딩하여 LCP를 개선하는 것
* 흔한 실수: FID를 개선하지 않고 입력에 대한 응답을 늦게 하는 것
* 성능 관련 주의사항: CLS를 개선하지 않아 사용자_experience가 저하되는 것

### 한 줄 정리
Web Vitals 최적화는 페이지 로딩 속도, 입력 응답 시간, 레이아웃 안정성을 개선하여 사용자 경험을하는 데 중요한 역할을 합니다.