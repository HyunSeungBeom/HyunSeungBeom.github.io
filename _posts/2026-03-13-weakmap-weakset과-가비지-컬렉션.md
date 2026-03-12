---
title: "[Deep Dive] WeakMap, WeakSet과 가비지 컬렉션"
date: 2026-03-13 08:09:07 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
WeakMap과 WeakSet은 자바스크립트에서 가비지 컬렉션을 효율적으로 처리할 수 있도록 도와주는 두 가지 타입입니다.

## Deep Dive

### 왜 필요한가?
- WeakMap과 WeakSet은 자바스크립트의 가비지 컬렉션 메커니즘과 연관된 문제를 해결하기 위해 필요합니다. 기존의 Map과 Set은 키와 값에 대한 강한 참조를 갖기 때문에, 가비지 컬렉션이 어려워집니다.
- 이전 방식의 한계는 메모리 누수가 쉽게 발생할 수 있고, 개발자가 직접 메모리 관리를 신경써야 한다는 점입니다.

### 내부 동작 원리
- WeakMap과 WeakSet은 약한 참조(weak reference)를 사용합니다. 약한 참조는 가비지 컬렉터가 객체를 삭제하여 메모리를 회수할 수 있도록 허용합니다.
- ASCII 다이어그램으로 시각화:
```
+---------------+
|  WeakMap    |
+---------------+
|  (키, 값)    |
|  약한 참조  |
+---------------+
       |
       |
       v
+---------------+
| 가비지 컬렉터  |
+---------------+
|  메모리 관리  |
+---------------+
```
- 이 다이어그램에서 WeakMap은 약한 참조를 사용하여 키와 값을 연결하고, 가비지 컬렉터는 약한 참조를 따라가며 메모리를 관리합니다.

### 코드로 이해하기

```typescript
// WeakMap 사용 예
let weakMap = new WeakMap();
let obj = { foo: 'bar' };
weakMap.set(obj, 'baz');
console.log(weakMap.get(obj)); // 'baz'

// 약한 참조로 인한 가비지 컬렉션
obj = null;
// 가비지 컬렉션 이후 weakMap에서 객체에 대한 참조가 제거됩니다.
```

```typescript
// 잘못된 사용 예: primitive 타입을 키로 사용하면 에러 발생
try {
  let weakMap = new WeakMap();
  weakMap.set('foo', 'bar'); // TypeError: Invalid value used as weak map key
} catch (e) {
  console.error(e);
}

// 올바른 사용 예: 객체를 키로 사용하면
let weakMap = new WeakMap();
let obj = {};
weakMap.set(obj, 'baz');
console.log(weakMap.get(obj)); // 'baz'
```

### 비교 분석

| 구분 | Map | WeakMap | Set | WeakSet |
|------|-----|---------|-----|---------|
| 키/값 참조 | 강한 참조 | 약한 참조 | 강한 참조 | 약한 참조 |
| 가비지 컬렉션 | 어려움 | 쉬움 | 어려움 | 쉬움 |
| 키 타입 | | 객체만 |  | 객체만 |

### 실전 팁
- Best Practice: WeakMap과 WeakSet을 사용하여 메모리 누수를 방지하고, 가비지 컬렉션을 효율적으로 처리합니다.
- 흔한 실수와 해결법: primitive 타입을 키로 사용하지 않고, 항상 객체를 키로 사용해야 합니다.
- 성능 관련 주의사항: 약한 참조로 인한 가비지 컬렉션이 발생할 수 있으므로, 성능에 민감한 코드에서는 사용에 주의해야 합니다.

### 한 줄 정리
WeakMap과 WeakSet은 약한 참조를 사용하여 가비지 컬렉션을 효율적으로 처리할 수 있도록 도와주는 자바스크립트의 두 가지 타입입니다.