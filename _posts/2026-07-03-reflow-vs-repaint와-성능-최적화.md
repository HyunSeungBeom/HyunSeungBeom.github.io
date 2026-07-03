---
title: "[Deep Dive] Reflow vs Repaint와 성능 최적화"
date: 2026-07-03 09:04:45 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Reflow와 Repaint는 웹 브라우저에서 렌더링할 때 발생하는 두 가지 주요 프로세스입니다.

## Deep Dive

### 왜 필요한가?
웹 브라우저는 사용자에게 화면을 표시하기 위해 다양한 요소를 렌더링해야 합니다. Reflow와 Repaint는 이러한 렌더링 프로세스를 효율적으로 처리하기 위한 두 가지 주요 메커니즘입니다. Reflow는 DOM의 레이아웃을 변경했을 때 발생하며, 모든 요소의 크기와 위치를 다시 계산하는 프로세스입니다. 반면, Repaint는 DOM 노드의 시각적 속성이 변경되었을 때 발생하며, 해당 노드의 스타일을 다시 적용하는 프로세스입니다. 이 두 가지 프로세스는 웹 브라우저의 성능을 최적화하는 데 중요한 역할을 합니다.

### 내부 동작 원리
Reflow와 Repaint의 내부 동작 원리를 이해하기 위해 다음의 ASCII 다이어그램을 참고하세요.
```
+---------------+
|  DOM Tree  |
+---------------+
       |
       |
       v
+---------------+
|  Layout Tree  |
+---------------+
       |
       |
       v
+---------------+
|  Paint Tree  |
+---------------+
       |
       |
       v
+---------------+
|  Rendering  |
+---------------+
```
위 다이어그램의 각 단계는 다음과 같은 역할을 수행합니다.
- DOM Tree: HTML 문서의 구조를 나타내는 트리 estruct
- Layout Tree: DOM Tree의 노드에 크기와 위치를 할당하는 트리
- Paint Tree: Layout Tree의 노드에 스타일을 적용하는 트리
- Rendering: Paint Tree의 노드를 실제 화면에 그리기

### 코드로 이해하기
다음의 TypeScript 코드는 Reflow와 Repaint의 차이를 보여주는 간단한 예제입니다.
```typescript
// 예제 1: Reflow 발생
const div = document.createElement('div');
div.style.width = '100px';
div.style.height = '100px';
document.body.appendChild(div);
// 이 시점에서 Reflow 발생

// 예제 2: Repaint 발생
div.style.backgroundColor = 'red';
// 이 시점에서 Repaint 발생
```
위 예제에서, `div` 요소를 추가할 때 Reflow가 발생하여 레이아웃이 갱신됩니다. 이후, `backgroundColor` 속성을 변경할 때 Repaint가 발생하여 스타일이 갱신됩니다.

### 비교 분석
다음 표는 Reflow와 Repaint의 특성을 비교합니다.
| 구분 | Reflow | Repaint |
|------|---|---|
| 발생 시점 | 레이아웃 변경시 | 스타일 변경시 |
| 영향 범위 | 전체 DOM 트리 | 변경된 노드만 |
| 성능 영향 | 높은 | 낮음 |

### 실전 팁
- 레이아웃 변경을 최소화하고, 스타일 변경만으로 갱신할 수 있도록 하여 Reflow의 발생을 줄입니다.
- 애니메이션과 같이 자주 갱신되는 요소는 `position: absolute` 또는 `position: fixed`를 사용하여 레이아웃의 영향을 줄입니다.
- 성능에 민감한 부분에서는 `requestAnimationFrame`를 사용하여 렌더링의 타이밍을 제어합니다.

### 한 줄 정리
Reflow와 Repaint는 웹 브라우저의 렌더링 프로세스를 최적화하기 위한 두 가지 주요 메커니즘으로, Reflow는 레이아웃 변경에 반응하고 Repaint는 스타일 변경에 반응하여 성능을 최적화합니다.