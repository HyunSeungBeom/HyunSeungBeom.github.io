---
title: "[Deep Dive] 브라우저 렌더링 파이프라인 (DOM, CSSOM, Render Tree, Layout, Paint, Composite)"
date: 2026-04-24 08:20:04 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
브라우저 렌더링 파이프은 브라우저가 사용자에게 콘텐츠를 렌더링하기 위해 수행하는 일련의 절차를 나타낸다.

## Deep Dive

### 왜 필요한가?
- 브라우저 렌더링 파이프라인은 브라우저가 콘텐츠를 사용자에게 효율적으로 렌더링하기 위해 필요하다. 이전 방식에서는 브라우저가 단순히 HTML과 CSS를 읽어서 화면에 그려내는 식으로 동작했지만, 이는 복잡한 콘텐츠와 대화형 웹애플리케이션의 요구에 따라 만족할 수 있는 성능을 내지 못했다.

### 내부 동작 원리
- 브라우저 렌더링 파이프라인은 다음과 같은 단계로 구성된다: 
  1. DOM : 브라우저는 HTML 문서를 읽어서 DOM(문서 객체 모델)을 생성한다.
  2. CSSOM : 브라우저는 CSS를 읽어서 CSSOM(CSS 객체 모델)을 생성한다.
  3. Render Tree 생성: 브라우저는 DOM과 CSSOM을 결합하여 Render Tree를 생성한다.
  4. Layout: 브라우저는 Render Tree의 각 요소의 크기와 위치를 계산한다.
  5. Paint: 브라우저는.Render Tree의 각 요소를 화면에 그린다.
  6. Composite: 브라우저는 그려진 요소들을 결합하여 최의 화면을 표시한다.

```
        +---------------+
        |  HTML 파싱  |
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
        |  CSS 파싱    |
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
        | Render Tree 생성|
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
        |  Paint        |
        +---------------+
                  |
                  |
                  v
        +---------------+
        |  Composite    |
        +---------------+
```

### 코드로 이해하기

```typescript
// 예시로 DOM 노드를 생성하고 Render Tree를 생성하는 단순한 예제
const html = '<div><p>안녕하세요</p></div>';
const parser = new DOMParser();
const doc = parser.parseFromString(html, 'text/html');
const dom = doc.body;

console.log(dom); // 생성된 DOM 노드 확인

// 이때부터는 브라우저의 내부 동작이므로 직접 구현하기는 어렵습니다.
// 브라우저 내부에서 DOM과 CSSOM을 Render Tree로 변환하는 과정을 나타내는 예시입니다.
function createRenderTree(dom, cssom) {
  // 실제 브라우저의 내부 동작을 구현하는 것은 매우 복잡하며,
  //  예시는 단순히 Render Tree 생성의 개념을 설명하기 위해 사용됩니다.
  const renderTree = [];
  // DOM의 각 노드와 CSSOM을 결합하여 Render Tree 생성
  // ...
  return renderTree;
}

const cssom = {}; // 실제 CSSOM 생성 구현은 생략
const renderTree = createRenderTree(dom, cssom);
console.log(renderTree); // 생성된 Render Tree 확인
```

```typescript
// 잘못된 사용 예: DOM을 자주 수정하여 렌더링 성능을 저하시키는 예
const container = document.getElementById('container');
for (let i = 0; i < 100; i++) {
  const div = document.createElement('div');
  div.textContent = `번호 ${i}`;
  container.appendChild(div);
}

// 올바른 사용 예: Document Fragment를 사용하여 렌더링 성능을 개선하는 예
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  const div = document.createElement('div');
  div.textContent = `번호 ${i}`;
  fragment.appendChild(div);
}
container.appendChild(fragment);
```

### 비교 분석

| 구분 | 브라우저 렌더링 파이프라인 | 다른 렌더링 메커니즘 |
|------|-------------------------|----------------------|
| 성능 | 빠르다               | 느리다               |
| 복잡도 | 복잡하다             | 단순하다             |
| 유연성 | 높은 유연성을 제공한다 | 낮은 유연성을 제공한다 |

### 실전 팁
- 브라우저가 렌더링 파이프라인을 수행하기전에, DOM에 변경을 많이 가하지 않도록 주의한다. 이는 브라우저의 리플로우와 리페인트를 유발하여 성능에 영향을 미칠 수 있다.
- CSS를 효과적으로 사용하여 브라우저의 렌더링 성능을 향상시킨다. 예를들면, `transform` 속성을 사용하여 리플로우를 피할 수 있다.
- 자바스크립트 코드를 최적화하여 DOM에 변경을 줄인다. 예를들면, Document Fragment를 사용하여 여러개의 DOM 노드를 한 번에 추가할 수 있다.

### 한 줄 정리
브라우저 렌더링 파이프라인은 브라우저가 효율적으로 콘텐츠를 렌더링하기 위해 수행하는 일련의 절차로, DOM 생성, CSSOM 생성, Render Tree 생성, Layout, Paint, Composite 등의 단계로 구성된다.