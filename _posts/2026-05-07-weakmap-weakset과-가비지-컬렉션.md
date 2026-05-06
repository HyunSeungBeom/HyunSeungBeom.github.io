---
title: "[Deep Dive] WeakMap, WeakSet과 가비지 컬렉션"
date: 2026-05-07 08:20:59 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
WeakMap과 WeakSet은 자바스크립트에서 가비지 컬렉션을 효율적으로 관리하는 데 사용되는 두 가지 자료구조입니다.

## Deep Dive

### 왜 필요한가?
- 메모리 누수를 방지하기 위해 필요합니다. 이전 방식에서는 객체를 삭제해도 다른 객체에 의해 참조되는 경우 메모리에서 해제되지 않기 때문에 WeakMap과 WeakSet이 이러한 문제를 해결하기 위해 도입되었습니다.

### 내부 동작 원리
- WeakMap과 WeakSet은 키 또는 요소로 사용되는 객체에 약한 참조(weak reference)를 유지합니다. 약한 참조란, 가비지 컬렉터가 해당 객체를 참조하는 다른 강한 참조가 없는 경우, 약한 참조만으로는 객체를 메모리에서 유지하지 않는다는 것을 의미합니다.
```
+---------------+
|  WeakMap    |
+---------------+
|  키: 객체   |
|  값: 객체   |
+---------------+
       |
       |
       v
+---------------+
|  약한 참조  |
+---------------+
       |
       |
       v
+---------------+
|  가비지 컬렉션|
+---------------+
```

### 코드로 이해하기

```typescript
// WeakMap 사용 예
const wm = new WeakMap();
const obj = { foo: 'bar' };
wm.set(obj, '');
console.log(wm.get(obj)); // ""
obj = null; // obj 참조 해제
// 가비지 컬렉터가 메모리에서 해제
```

```typescript
// 잘못된 사용 예: primitive 타입 사용 시
const wm = new WeakMap();
wm.set('문자열', '값'); // TypeError: Invalid value used as weak map key
```

```typescript
// 올바른 사용 예: 객체 사용 시
const wm = new WeakMap();
const obj = {};
wm.set(obj, '값');
```

### 비교 분석

| 구분 | WeakMap | WeakSet | Map | Set |
|------|---------|---------|-----|-----|
| 키/요소 | 객체     | 객체    | | |
| 값     |      | -       | | -   |
| 약한 참조 | O       | O       | X   | X   |

### 실전 팁
- WeakMap과 WeakSet을 사용하여 메모리 누수를 방지할 수 있습니다.
- WeakMap과 WeakSet의 키/요소로 사용되는 객체는 메모리에서 해제될 수 있으므로, 사용 시 주의가 필요합니다.
- 성능 관련 주의사항으로, WeakMap과 WeakSet의 크기는 정확히 측정되지 않으므로, 성능 최적화에 신경 써야 할 수 있습니다.

### 한 줄 정리
WeakMap과 WeakSet은 약한 참조를 유지하는 자료구조로, 메모리 누수를 방지하는 데 사용됩니다.