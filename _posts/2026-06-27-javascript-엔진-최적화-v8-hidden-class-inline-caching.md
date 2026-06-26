---
title: "[Deep Dive] JavaScript 엔진 최적화 (V8 Hidden Class, Inline Caching)"
date: 2026-06-27 08:29:08 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript 엔진 최적화에서 V8 setHidden Class와 Inline Caching을 사용하면 성능을 개선할 수 있다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: JavaScript의 동적 타입과 프로퍼티 접근의 비용을 줄이는 것
- 이전 방식의 한계: JavaScript 엔진에서 동적 타입 체크와 프로퍼티 접근이 발생하면 성능이 저하된다.

### 내부 동작 원리
- 핵심 메커니즘 설명: V8 엔진은 객체의 프로퍼티 구조를 분석하여 Hidden Class를 생성하고, 이에 따라 Inline Caching을 수행한다.
- ASCII 다이어그램으로 시각화:
```
+---------------+
|  JavaScript  |
|  (동적 타입) |
+---------------+
       |
       |
       v
+---------------+
|  V8 엔진    |
|  (Hidden Class) |
+---------------+
       |
       |
       v
+---------------+
|  Inline Caching |
|  (프로퍼티 접근) |
+---------------+
```

### 코드로 이해하기

```typescript
// 실제 동작을 보여주는 코드 예제
class Person {
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

const person = new Person('John', 30);
console.log(person.name); // Inline Caching 사용
```

```typescript
// 잘못된 사용 예: Dynamic 프로퍼티 추가
class Person {
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

const person = new Person('John', 30);
person.address = 'Seoul'; // Hidden Class 변경
console.log(person.name); // Inline Caching 실패
```

```typescript
// 올바른 사용 예: 프로퍼티 구조 일치
class Person {
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

const person1 = new Person('John', 30);
const person2 = new Person('Jane', 25);
console.log(person1.name); // Inline Caching 사용
console.log(person2.name); // Inline Caching 사용
```

### 비교 분석

| 구분 | Dynamic 프로퍼티 | Static 프로퍼티 | Hidden Class |
|------|------------------|----------------|--------------|
| 성능 | 낮음 | 높음 | 높음 |
| 사용 예 | `person.address = 'Seoul'` | `class Person { address: string }` | `const person = new Person('John', 30)` |
| Inline Caching | 실패 | 성공 | 성공 |

### 실전 팁
- Best Practice: 객체의 프로퍼티 구조를 일관 있게 mantenain 한다.
- 흔한 실수와 해결법: Dynamic 프로퍼티 추가를 피한다.
- 성능 관련 주의사항: 프로퍼티 접근 시 Inline Caching이 실패하지 않도록 한다.

### 한 줄 정리
V8 엔진의 Hidden Class와 Inline Caching을 사용하여 JavaScript의 동적 타입과 프로퍼티 접근의 비용을 줄일 수 있다.