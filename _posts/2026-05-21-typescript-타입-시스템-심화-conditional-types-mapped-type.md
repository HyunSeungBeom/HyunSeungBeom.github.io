---
title: "[Deep Dive] TypeScript 타입 시스템 심화 (Conditional Types, Mapped Types, Template Literal Types)"
date: 2026-05-21 08:31:00 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
TypeScript 타입 시스템은 Conditional Types, Mapped Types, Template Literal Types를 통해 복잡한 코드의 안정성을 높일 수 있다.

## Deep Dive

### 왜 필요한가?
- 이전 버전의 TypeScript에서는 타입 시스템이 제한적이어서 복잡한 타입을 표현하기 어려웠다.
- Conditional Types, Mapped Types, Template Literal Types는 이러한 한계를 보완하여 복잡한 타입을 표현하고 코드의 안정성을 높일 수 있다.

### 내부 동작 원리
- TypeScript의 타입 시스템은 런타임에 영향을 미치지 않고, 컴파일 타임에만 작동한다.
- Conditional Types는 조건에 따라 타입을 결정하며, Mapped Types는 기존 타입을 변형하여 새로운 타입을 생성한다.
- Template Literal Types는 문자열과 함께 타입을 조합하는 기능을 제공한다.

```
          +---------------+
          |  TypeScript  |
          +---------------+
                  |
                  |
                  v
+-----------------------+       +---------------+
|  Conditional Types  |-------|  Type Checking  |
+-----------------------+       +---------------+
                  |
                  |
                  v
+-----------------------+       +---------------+
|  Mapped Types        |-------|  Type Creation  |
+-----------------------+       +---------------+
                  |
                  |
                  v
+-----------------------+       +---------------+
|  Template Literal    |-------|  Type Combination|
|  Types              |       +---------------+
+-----------------------+
```

### 코드로 이해하기

```typescript
// Conditional Types
type IsString<T> = T extends string ? true : false;
type result1 = IsString<'hello'>; // true
type result2 = IsString<123>; // false
```

```typescript
// Mapped Types
type Options<T> = {
  [P in keyof T]: T[P] | null;
};
interface User {
  name: string;
  age: number;
}
type UserOptions = Options<User>;
// type UserOptions = {
//   name: string | null;
//   age: number | null;
// }
```

```typescript
// Template Literal Types
type World = 'world';
type Greeting = `hello ${World}`;
// type Greeting = 'hello world'
```

```typescript
// 잘못된 사용 예
// TypeScript는 런타임에 영향을 미치지 않기 때문에, 타입만으로 런타임에 발생하는 오류를 예방하기 어렵다.
// 올바른 사용 예
// 복잡한 타입을 표현하고, 코드의 안정성을 높일 수 있다.
```

### 비교 분석

| 구분 | Conditional Types | Mapped Types | Template Literal Types |
|------|-------------------|--------------|-------------------------|
| 설명 | 조건에 따라 타입을 결정 | 기존 타입을 변형하여 새로운 타입을 생성 | 문자열과 함께 타입을 조합 |
| 사용 예 | 타입 가드 | 옵션 타입 생성 | 문자열 타입 조합 |
| 장점 | 타입을 동적으로 결정 | 복잡한 타입을 간결하게 표현 | 문자열 타입을 조합하여 새로운 타입 생성 |

### 실전 팁
- Conditional Types를 사용하여 타입을 동적으로 결정할 수 있다.
- Mapped Types를 사용하여 복잡한 타입을 간결하게 표현할 수 있다.
- Template Literal Types를 사용하여 문자열 타입을 조합하여 새로운 타입을 생성할 수 있다.
- TypeScript의 타입 시스템은 런타임에 영향을 미치지 않기 때문에, 타입만으로 런타임에 발생하는 오류를 예방하기 어렵다.

### 한 줄 정리
TypeScript의 Conditional Types, Mapped Types, Template Literal Types를 사용하여 복잡한 코드의 안정성을 높일 수 있다.