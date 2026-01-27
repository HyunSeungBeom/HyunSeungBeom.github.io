---
title: "[Deep Dive] Critical Rendering Path 최적화 전략"
date: 2026-01-21 23:08:17 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Critical Rendering Path(CRP) 최적화 전략은 빠른 웹 페이지 렌더링을 위해 브라우저의 렌더링 과정을 분석하고 최적화하는 전략입니다.

## Deep Dive

### 왜 필요한가?
CRP 최적화 전략은 브라우저의 렌더링 과정이 느려지는 문제를 해결합니다. 이전 방식에서는 브라우저의 렌더링 과정이 복잡하고 느려서 사용자에게 느린 성능으로 느껴졌습니다. 하지만 CRP 최적화 전략을 사용하면 브라우저의 렌더링 과정을 최적화하여 빠른 웹 페이지 렌더링을 구현할 수 있습니다.

### 내부 동작 원리
CRP 최적화 전략은 브라우저의 렌더링 과정을 분석하여 렌더링 병목현상을 식별하고 최적화합니다. 브라우저의 렌더링 과정을 다음과 같은ASCII 다이어그램으로 시각화할 수 있습니다.

```
                      +---------------+
                      |  HTML Parsing  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  CSS Parsing   |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  JavaScript Execution |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Layout Calculation |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Painting       |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Compositing    |
                      +---------------+
```

### 코드로 이해하기
CRP 최적화 전략을 코드로 보여주는 예제입니다.
```typescript
// CSS 파일을 비동기적으로 로딩하기
const cssLink = document.createElement('link');
cssLink.rel = 'stylesheet';
cssLink.href = 'style.css';
document.head.appendChild(cssLink);

// JavaScript 파일을 비동기적으로 로딩하기
const jsScript = document.createElement('script');
jsScript.src = 'script.js';
document.body.appendChild(jsScript);
```

```typescript
// 잘못된 사용 예: CSS 파일을 동기적으로 로딩하기 (❌)
const cssLink = document.createElement('link');
cssLink.rel = 'stylesheet';
cssLink.href = 'style.css';
document.head.appendChild(cssLink);
document.write('<style>body { background-color: #f2f2f2; }</style>');

// 올바른 사용 예: CSS 파일을 비동기적으로 로딩하기 (✅)
const cssLink = document.createElement('link');
cssLink.rel = 'stylesheet';
cssLink.href = 'style.css';
cssLink.onload = function() {
  document.write('<style>body { background-color: #f2f2f2; }</style>');
};
document.head.appendChild(cssLink);
```

### 비교 분석
다음 표는 CRP 최적화 전략의 비교 분석입니다.

| 구분 | 동기 로딩 | 비동기 로딩 | Code Splitting |
|------|---|---|---|
| 렌더링 성능 | 느림 | 빠름 | 빠름 |
| 자원 로딩 방법 | 동기적 | 비동기적 | 비동기적 |
| 파일 분할 | 없음 | 없음 | 있음 |

### 실전 팁
- Best Practice: CSS 파일을 비동기적으로 로딩하고, JavaScript 파일은 body 태그의 맨 밑에 위치시키는 것이 좋습니다.
- 흔한 실수: CSS 파일을 동기적으로 로딩하거나, JavaScript 파일을 head 태그에 위치시키는 것입니다.
- 성능 관련 주의사항: CRP 최적화 전략을 사용할 때, 렌더링 성능을 주의해서 분석해야 합니다.

### 한 줄 정리
CRP 최적화 전략은 브라우저의 렌더링 과정을 분석하여 렌더링 병목현상을 식별하고 최적화하여 빠른 웹 페이지 렌더링을 구현하는 전략입니다.