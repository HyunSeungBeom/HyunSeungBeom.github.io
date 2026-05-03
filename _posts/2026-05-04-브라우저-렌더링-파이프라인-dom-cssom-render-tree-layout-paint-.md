---
title: "[Deep Dive] 브라우저 렌더링 파이프라인 (DOM, CSSOM, Render Tree, Layout, Paint, Composite)"
date: 2026-05-04 08:18:42 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
브라우저 렌더링 파이프라인은 브라우저가 웹 페이지를 렌더링하는 과정을 말한다.

## Deep Dive

### 왜 필요한가?
브라우저 렌더링 파이프은 웹 페이지의 구조와 스타일을 해석하여 사용자에게 보여주는 과정을 포함한다. 이전에는 브라우저가 페이지를 렌더링하는 데에 큰 어려움이있었다. 렌더링 파이프라인을 사용하면 브라우저가 페이지를 빠르고 정확하게 렌더링할 수 있다.

### 내부 동작 원리
브라우저 렌더링 파이프은 다음과 같은 단계로 구성된다.
1. DOM(Document Object Model) 생성: 브라우저가 HTML 문서를 해석하여 DOM 트리를 생성한다.
2. CSSOM(CSS Object Model) 생성: 브라우저가 CSS를 해석하여 CSSOM 트리를 생성한다.
3. Render Tree 생성: 브라우저가 DOM과 CSSOM을 결합하여 Render Tree를 생성한다.
4. Layout: 브라우저가 Render Tree를 기반으로 페이지의 레이아웃을 계산한다.
5. Paint: 브라우저가 페이지의 각 요소를 그래픽으로 그린다.
6. Composite: 브라우저가 페이지의 각 요소를 합성하여 최적인 페이지를 생성한다.

```
      +---------------+
      |  HTML문서   |
      +---------------+
            |
            |
            v
      +---------------+
      |  DOM 생성    |
      +---------------+
            |
            |
            v
      +---------------+
      |  CSS 해석    |
      +---------------+
            |
            |
            v
      +---------------+
      |  CSSOM 생성  |
      +---------------+
            |
            |
            v
      +---------------+
      |  Render Tree  |
      +---------------+
            |
            |
            v
      +---------------+
      |  Layout 계산  |
      +---------------+
            |
            |
            v
      +---------------+
      |  Paint화  |
      +---------------+
            |
            |
            v
      +---------------+
      |  Composite 합성|
      +---------------+
            |
            |
            v
      +---------------+
      |  페이지 렌더링  |
      +---------------+
```

### 코드로 이해하기
```typescript
// DOM 생성 예
const dom = new DOMParser().parseFromString('<html><body>Hello World!</body></html>', 'text/html');

// CSSOM 생성 예
const cssom = new CSSStyleSheet();
cssom.replaceSync('body { background-color: #f2f2f2; }');
```

```typescript
// 잘못된 사용 예: DOM을 과도하게 업데이트 하는 경우
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = 'Hello World!';
  document.body.appendChild(div);
}

// 올바른 사용 예: DOM을 배치하고 한번에 업데이트하는 경우
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = 'Hello World!';
  fragment.appendChild(div);
}
document.body.appendChild(fragment);
```

### 비교 분석

| 구분 | DOM | CSSOM | Render Tree |
|------|---|---|---|
| 역할 | 문서구조 | 스타일 | 렌더링 트리 |
| 생성 | HTML 해석 | CSS 해석 | DOM과 CSSOM 결합 |
| 사용 | 렌더링 | 레이아웃 계산 | 페이지 렌더링 |

### 실전 팁
- DOM을 과도하게 업데이트 하는 경우 성능 문제가 발생할 수 있으므로, DOM을 배치하고 한번에 업데이트하는 것이 좋다.
- CSS를 외부 파일로 분리하여 브라우저가 동시에 다운로드할 수 있도록 한다.
- 레이아웃을 계산하는 단계에서 많은 시간이 소요될 수 있으므로, 레이아웃을 최적화하는 것이 중요하다.

### 한 줄 정리
브라우저 렌더링 파이프라인은 브라우저가 웹 페이지를 렌더링하는 과정을 포함하며, DOM 생성, CSSOM 생성, Render Tree 생성, 레이아웃 계산, 그림 그리기, 합성의 단계로 구성된다.