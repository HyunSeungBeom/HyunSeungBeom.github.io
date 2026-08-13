---
title: "[Deep Dive] TypeScript 컴파일러 동작 원리와 Declaration Files"
date: 2026-08-14 08:40:02 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
TypeScript 컴파일러 동작 원리와 Declaration Files는 TypeScript를 효과적으로 사용하기 위한 중요한 개념입니다.

## Deep Dive

### 왜 필요한가?
TypeScript 컴파일러는 TypeScript 코드를 JavaScript 코드로 변환합니다. 이는 브라우저나 Node.js에서 실행할 수 있지만, TypeScript 자체로는 실행되지 않기 때문입니다. Declaration Files는 external 모듈에서 제공하는 API의 타입 정보를 제공합니다. 이는 TypeScript를 사용하는 개발자가 external 모듈의 함수나 변수의 타입을 알 수 있도록 해주고, TypeScript의 타입 체크를 가능하게 합니다.

이전 방식, JavaScript만으로 개발되면, 코드의 구조와 타입을 알기 어렵고, 런타임에 오류가 발생할 수 있습니다. TypeScript와 Declaration Files를 사용하면 이러한 문제를 해결할 수 있습니다.

### 내부 동작 원리
TypeScript 컴파일러는 다음 단계로 동작합니다.
1. 파서(Parser): 소스 코드를 파싱하여 AST(Abstract Syntax Tree)를 생성합니다.
2. 바인더(Binder): AST를 분석하여 바인딩 정보를 생성합니다.
3. 체커(Checker): 바인딩 정보를 사용하여 코드의 타입을 체크합니다.
4. 발급자(Emitter): 타입 체크된 코드를 JavaScript로 변환합니다.

Declration Files는 모듈의 exports에 대한 타입 정보를 제공합니다. 이를 통해 TypeScript 컴파일러는 external 모듈의 함수나 변수의 타입을 알 수 있습니다.
```
               +---------------+
               |  TypeScript  |
               +---------------+
                     |
                     |
                     v
               +---------------+
               |  Parser      |
               |  (AST 생성)  |
               +---------------+
                     |
                     |
                     v
               +---------------+
               |  Binder      |
               |  (바인딩 정보 생성)|
               +---------------+
                     |
                     |
                     v
               +---------------+
               |  Checker     |
               |  (타입 체크)  |
               +---------------+
                     |
                     |
                     v
               +---------------+
               |  Emitter     |
               |  (JavaScript 변환)|
               +---------------+
                     |
                     |
                     v
               +---------------+
               |  Declaration  |
               |  Files (타입 정보 제공)|
               +---------------+
```

### 코드로 이해하기
```typescript
// Declaration Files의 예
// file: my-module.d.ts
declare module 'my-module' {
  export function add(a: number, b: number): number;
}
```

```typescript
// 사용 예
// file: main.ts
import { add } from 'my-module';

const result = add(1, 2);
console.log(result);
```

```typescript
// Declaration Files 사용하지 않을 경우
// file: main.ts
import { add } from 'my-module';

// @ts-ignore: Could not find a declaration file for module 'my-module'.
const result = add(1, 2);
console.log(result);
```

```typescript
// 올바른 Declaration Files 사용 예
// file: main.ts
import { add } from 'my-module';

// Type checking이 동작합니다.
const result: number = add(1, 2);
console.log(result);
```

### 비교 분석

| 구분 | TypeScript | JavaScript |
|------|------------|-------------|
| 타입 체크 | 가능       | 불가능      |
| Declaration Files | 필요      | 불필요     |
| 코드 구조 | 명확      | 불명확     |

### 실전 팁
- Declaration Files는 external 모듈에서 제공하는 API의 타입 정보를 제공하기 위해 사용해야 합니다.
- TypeScript를 사용할 경우, Declaration Files를 사용하여 타입 체크를 가능하게 해야 합니다.
- Declaration Files를 잘 관리하지 않으면, 타입 체크가 동작하지 않아 런타임에 오류가 발생할 수 있습니다.

### 한 줄 정리
TypeScript 컴파일러와 Declaration Files는 TypeScript로 개발할 때 중요한 개념이며, 효과적으로 사용하면 코드의 구조와 타입을 알 수 있고, 런타임에 오류를 줄일 수 있습니다.