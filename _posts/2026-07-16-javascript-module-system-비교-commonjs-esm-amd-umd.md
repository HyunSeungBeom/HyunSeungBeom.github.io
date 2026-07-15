---
title: "[Deep Dive] JavaScript Module System 비교 (CommonJS, ESM, AMD, UMD)"
date: 2026-07-16 08:57:40 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript Module System은 자바스크립트 코드를 모듈화하여 관리하고 재사용할 수 있도록 하는 시스템이다.

## Deep Dive

### 왜 필요한가?
JavaScript Module System은 자바스크립트 코드의 모듈화를 가능하게 하여 코드를 더 효율적으로 관리하고 재사용할 수 있다. 이전 방식에서는 전역 변수와 함수를 사용하여 코드를 작성했지만, 이 방식은 코드의 복잡도가 증가하고 관리가 어려워지는 문제가 있었다. JavaScript Module System은 이러한 문제를 해결하기 위해 등장했다.

### 내부 동작 원리
JavaScript Module System의 핵심 메커니즘은 모듈을 로딩하고 exports, imports하는 것이다. 다음의 ASCII 다이어그램으로 시각화할 수 있다.
```
+---------------+
|  Module A    |
+---------------+
        |
        |  exports
        v
+---------------+
|  Module B    |
|  (import A)  |
+---------------+
        |
        |  exports
        v
+---------------+
|  Module C    |
|  (import B)  |
+---------------+
```
위 다이어그램에서 Module A는 Module B에 exports를 제공하고, Module B는 Module C에 exports를 제공한다. Module C는 Module B의 exports를 imports하여 사용할 수 있다.

### 코드로 이해하기
```typescript
// Module A
export function add(a: number, b: number) {
  return a + b;
}

// Module B
import { add } from './ModuleA';
export function multiply(a: number, b: number) {
  return a * b;
}

// Module C
import { multiply } from './ModuleB';
import { add } from './ModuleA';
console.log(multiply(2, 3)); // 6
console.log(add(2, 3)); // 5
```
위 코드에서 Module A는 add 함수를 exports한다. Module B는 Module A의 add 함수를 imports하여 multiply 함수를 exports한다. Module C는 Module B의 multiply 함수와 Module A의 add 함수를 imports하여 사용한다.

```typescript
// 잘못된 사용 예
import { add } from './ModuleA';
const result = add(2, '3'); // type error

// 올바른 사용 예
import { add } from './ModuleA';
const result = add(2, 3); // 5
```
위 코드에서 잘못된 사용 예는 type error가 발생한다. 올바른 사용 예는 add 함수를 제대로 사용한다.

### 비교 분석
| 구분 | CommonJS | ESM | AMD | UMD |
|------|---------|-----|-----|-----|
| 로딩 방식 | 동기식 | 비동기식 | 비동기식 | 동기식/비동기식 |
| 모듈 정의 | require | import | define | umd |
| 브라우저 지원 | X | O | O | O |

### 실전 팁
- Best Practice: ESM을 사용하여 모듈을 정의한다.
- 흔한 실수: CommonJS와 ESM을 혼용하여 사용한다.
- 성능 관련 주의사항: 모듈 로딩 시간을 최적화하기 위해 Tree Shaking을 사용한다.

### 한 줄 정리
JavaScript Module System은 자바스크립트 코드를 모듈화하여 관리하고 재사용할 수 있도록 하는 시스템으로, ESM을 사용하여 모듈을 정의하는 것이 Best Practice이다.