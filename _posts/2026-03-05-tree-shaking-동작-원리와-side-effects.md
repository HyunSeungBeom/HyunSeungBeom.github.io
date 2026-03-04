---
title: "[Deep Dive] Tree Shaking 동작 원리와 Side Effects"
date: 2026-03-05 08:10:19 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Tree Shaking은 불필요한 코드를 제거하여 번들 사이즈를 줄이는 기술입니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 불필요한 코드로 인한 번들 사이즈 증가 문제
- 이전 방식의 한계: 코드를 전체적으로 번들링하여 파일 크기가 거대해지는 문제

Tree Shaking은 코드에서 실제로 사용하지 않는 부분을 자동으로 제거하여 번들 사이즈를 최적화하는 기술입니다. 로 웹 애플리케이션의 로딩 속도가 개선되고 사용자 경험을 향상시킬 수 있습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Tree Shaking은 ES6 모듈 구문을 분석하여 실제로 사용되는 코드만 번들링합니다.
- ASCII 다이어그램으로 시각화:
```
                      +---------------+
                      |  애플리케이션  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  ES6 모듈 구문  |
                      |  분석 및 파싱  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  사용 코드 식별  |
                      |  unused 코드 제거  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  최적화된 번들  |
                      +---------------+
```

### 코드로 이해하기

```typescript
// tree-shaking.ts
export function add(a: number, b: number) {
  return a + b;
}

export function subtract(a: number, b: number) {
  return a - b;
}
```

```typescript
// main.ts
import { add } from './tree-shaking';

console.log(add(2, 3)); // 5
```

```typescript
// 잘못된 사용 예: unused 코드가 포함된 경우
import { add, subtract } from './tree-shaking';
console.log(add(2, 3)); // 5

// 올바른 사용 예: unused 코드가 제거된 경우
import { add } from './tree-shaking';
console.log(add(2, 3)); // 5
```

### 비교 분석

| 구분 | 사용 전 | 사용 후 |
|------|---------|---------|
| 번들 사이즈 | 100KB    | 50KB    |
| 로딩 속도  | 2초      | 1초     |
| 사용자 경험 | 느림     | 개선   |

### 실전 팁
- Best Practice: ES6 모듈 구문을 사용하고 unused 코드를 최대한 제거하여 Tree Shaking의 효과를 극대화합니다.
- 흔한 실수와 해결법: unused 코드가 포함되었을 경우, unused 코드를 제거하거나 사용하지 않는 코드를 별도 파일로 분리합니다.
- 성능 관련 주의사항: Tree Shaking은 번들 사이즈를 줄여 로딩 속도를 개선하지만, 복잡한 코드 구조일 경우 오히려 성능이 저하될 수 있으므로 주의가 필요합니다.

### 한 줄 정리
Tree Shaking은 ES6 모듈 구문을 분석하여 unused 코드를 자동으로 제거하여 번들 사이즈를 최적화하고, 웹 애플리케이션의 로딩 속도와 사용자 경험을 향상시킵니다.

---