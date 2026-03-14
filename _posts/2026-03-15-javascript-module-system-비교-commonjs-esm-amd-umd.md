---
title: "[Deep Dive] JavaScript Module System 비교 (CommonJS, ESM, AMD, UMD)"
date: 2026-03-15 08:09:04 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript Module System은 JavaScript 코드를 구조화하고 재사용하기 위한 모듈화 시스템으로, 주요 종류로는 CommonJS, ESM, AMD, UMD가 있다.

## Deep Dive

### 왜 필요한가?
JavaScript 코드의 모듈화는 유지 보수와 코드 재사용성을 높이기 위해 필요하다. 이전에는 전역 변수와 함수를 사용하여 코드를 관리했지만, 이는 코드의 규모가 커질수록 관리가 어려워지고, 네임스페이스 충돌 등의 문제가 발생했다. 모듈 시스템은 이러한 문제를 해결하기 위해 등장했다.

### 내부 동작 원리
모듈 시스템의 핵심은 모듈을 로드하고, 의존성을 관리하는 것이다. 각 모듈은 독립적인 Scope를 가지고, 필요한 모듈을 import하여 사용할 수 있다. 다음 ASCII 다이어그램은 모듈 로딩과 의존성 관리의 과정을 보여준다.
```
                 +---------------+
                 |  모듈 로더  |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  모듈 A    |
                 |  (의존성: B) |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  모듈 B    |
                 |  (의존성: C) |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  모듈 C    |
                 |  (의존성: 없음) |
                 +---------------+
```

### 코드로 이해하기
다음은 실제 사용 예를 보여주는 TypeScript 코드이다.
```typescript
// 모듈 A
import { funcB } from './moduleB';
export function funcA() {
  funcB();
}

// 모듈 B
import { funcC } from './moduleC';
export function funcB() {
  funcC();
}

// 모듈 C
export function funcC() {
  console.log('funcC 호출');
}
```
잘못된 사용 예로, 다음과 같이 모듈이 서로 참조할 경우 참조 오류가 발생할 수 있다.
```typescript
// 모듈 A
import { funcB } from './moduleB';
export function funcA() {
  funcB();
}

// 모듈 B
import { funcA } from './moduleA';
export function funcB() {
  funcA();
}
```
올바른 사용 예는 모듈이 서로 참조할 때, 중간에 다른 모듈을 거치거나, 의존성을 해결하는 방법을 사용하는 것이다.

### 비교 분석
다음 표는 주요 모듈 시스템 비교한다.
| 구분 | CommonJS | ESM | AMD | UMD |
|------|---------|-----|-----|-----|
| 로딩 방식 | 동적 로딩 | 정적 로딩 | 동적 로딩 | 동적/정적 로딩 |
| 지원 브라우저 | 대부분 | 브라우저 | 대부분 | 대부분 |
| 지원 환경 | Node.js | 브라우저/Node.js | 브라우저 | 브라우저/Node.js |

### 실전 팁
- 가능한 한 정적 로딩을 사용하여 코드 최적화를 향상시킨다.
- 모듈 이름과 파일 이름을 일치시키는 것이 좋다.
- 의존성 관리를 위한 도구를 사용한다.
- 브라우저와 Node.js 환경에서 모두 사용 가능하도록 코드를 작성한다.

### 한 줄 정리
JavaScript Module System은 코드의 유지 보수와 재사용성을 높이기 위해 다양한 모듈 시스템을 제공하며, 각각의 장단점을 파악하여 적절한가 필요하다.