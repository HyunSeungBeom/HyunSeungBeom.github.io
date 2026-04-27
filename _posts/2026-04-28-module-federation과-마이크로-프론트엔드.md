---
title: "[Deep Dive] Module Federation과 마이크로 프론트엔드"
date: 2026-04-28 08:21:53 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Module Federation과 마이크로 프론트엔드란 독립적인 프론트엔드 애플리케이션을 모듈화하여 하나의 애플리케이션으로 동작시키는 기술이다.

## Deep Dive

### 왜 필요한가?
- 기존의 모노리틱 아키텍처에서는 애플리케이션을 하나의 단위로 개발하여 유지보수하므로, 일부 모듈의 변경이 전체 애플리케이션에 영향을 미치게 된다. Module Federation과 마이크로 프론트엔드가 필요한 이유는 이러한 모노리틱 아키텍처의 한계를 해결하기 위해서이다.
- 모듈별로 개발과 배포를 독립적으로 수행할 수 있으므로, 개발 팀의 효율성을하고, 배포의 빈번함을 가능하게 한다.

### 내부 동작 원리
- Module Federation은 웹팩(webpack) 등의 모듈 번들러를 기반으로 하며, 각 모듈은 하나의 독립적인 애플리케이션으로 개발된다.
- ASCII 다이어그램으로 시각화하면 다음과 같다:
```
          +---------------+
          |  Module A    |
          +---------------+
                  |
                  |  Export
                  v
          +---------------+
          |  Module B    |
          +---------------+
                  |
                  |  Import
                  v
          +---------------+
          |  Container  |
          +---------------+
```
- Module A와 Module B는 각각 독립적인 애플리케이션이며, Container는 이러한 모듈들을 하나의 애플리케이션으로 동작시키는 역할을 한다.

### 코드로 이해하기
```typescript
// Module A
export const moduleName = 'Module A';
export function sayHello() {
  console.log('Hello from Module A');
}

// Module B
import { moduleName, sayHello } from './Module A';
console.log(moduleName);
sayHello();
```

```typescript
// 잘못된 사용 예
// Module A
export const moduleName = 'Module A';
export function sayHello() {
  console.log('Hello from Module A');
}

// Module B
import { moduleName } from './Module A';
console.log(moduleName);
// sayHello 함수를 사용하지 않아도 불러오기가 발생한다.
```

```typescript
// 올바른 사용 예
// Module A
export const moduleName = 'Module A';
export function sayHello() {
  console.log('Hello from Module A');
}

// Module B
import { moduleName, sayHello } from './Module A';
console.log(moduleName);
sayHello();
// 필요한 모듈만 불러온다.
```

### 비교 분석

| 구분 | 모노리틱 아키텍처 | 마이크로 프론트엔드 |
|------|---|---|
| 개발율 | 낮다 | 높다 |
| 배포 빈번함 | 낮다 | 높다 |
| 유지보수 | 어렵다 | 쉽다 |
| 확장성 | 낮다 | 높다 |

### 실전 팁
-_best Practice_: 모듈 간 의존성을 최소화하는 설계를 고려해야 한다.
-_흔한 실수와 해결법_: 모듈 간의 의존성을 제대로 관리하지 않아, 충돌이 발생하는 경우가 있다. 이를 해결하기 위해 의존성 관리 툴을 사용하면 된다.
-_성능 관련 주의사항_: 모듈의 크기가 너무 크면, 로딩 시간이 길어질 수 있다. 이를 해결하기 위해 코드 스플리팅(Code Splitting) 등을 사용하면 된다.

### 한 줄 정리
Module Federation과 마이크로 프론트엔드는 독립적인 프론트엔드 애플리케이션을 모듈화하여 하나의 애플리케이션으로 동작시키는 기술로, 개발 효율성을 높이고, 배포의 빈번함을 가능하게 하며, 유지보수를 쉽게 한다.