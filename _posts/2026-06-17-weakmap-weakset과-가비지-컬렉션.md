---
title: "[Deep Dive] WeakMap, WeakSet과 가비지 컬렉션"
date: 2026-06-17 08:33:53 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
WeakMap, WeakSet은 자바스크립트에서 가비지 컬렉션을 효율적으로 관리할 수 있는 두 가지 종류의 자료구조입니다.

## Deep Dive

### 왜 필요한가?
- WeakMap과 WeakSet은 자바스크립트의 가비지 컬렉션을 효율적으로 관리할 수 있게 해주는 두 가지 자료구조입니다. 이전에는 이러한 관리가 쉽지 않았습니다. 특히 Map과 Set을 사용할 때 키나 값이 객체일 경우, 참조 카운트를 증가시키므로 가비지 컬렉션이 어려워졌습니다.
- 이전 방식의 한계는 메모리 누수가 쉽게 발생할 수 있다는 점입니다. WeakMap과 WeakSet이 이런 문제를 해결해 줄 수 있습니다.

### 내부 동작 원리
- WeakMap과 WeakSet은 키 또는 값으로 객체를 사용했을 때, 가비지 컬렉터가 해당 객체를 메모리에서 제거할 수 있도록 허용하는 특성이 있습니다. 이러한 특성은 내부 참조 카운트를 관리하는 방식과 관련이 있습니다.
```
  +---------------+
  |  키(Object)  |
  +---------------+
           |
           |
           v
  +---------------+
  |  WeakMap/Set  |
  +---------------+
           |
           |
           v
  +---------------+
  | 가비지 컬렉터  |
  +---------------+
```

### 코드로 이해하기

```typescript
// 예시: WeakMap 사용법
const weakMap = new WeakMap<object, string>();
const obj = { foo: 'bar' };
weakMap.set(obj, 'hello');

// obj 참조를 제거하면 가비지 컬렉션이 가능해집니다.
obj = null;
```

```typescript
// 잘못된 사용 예: 객체를 참조하는 다른 변수로 인해 가비지 컬렉션이 되지 않음
const wrongExample = new WeakMap<object, string>();
const obj2 = { foo: 'bar' };
wrongExample.set(obj2, 'world');
const anotherReference = obj2; // 여전히 obj2를 참조하고 있으므로 가비지 컬렉션이 되지 않습니다.
obj2 = null;
```

```typescript
// 올바른 사용 예: WeakSet을 사용하여 가비지 컬렉션 제어
const weakSet = new WeakSet<object>();
const obj3 = { foo: 'baz' };
weakSet.add(obj3);
// obj3을 참조하는 변수가 더 이상 없으면 가비지 컬렉션이 가능해집니다.
obj3 = null;
```

### 비교 분석

| 구분 | Map | WeakMap | Set | WeakSet |
|------|-----|---------|-----|---------|
| 키 또는 값 참조 | 강한 참조 | 약한 참조 | 강한 참조 | 약한 참조 |
| 가비지 컬렉션 | 방해 | 허용 | 방해 | 허용 |
| 사용 예 | 일반적인 데이터 저장 | 객체의 임시 메타데이터 저장 | 고유한 객체 집합 | 임시로 객체를 추적 |

### 실전 팁
- 약한 참조를 사용할 때는 언제 가비지 컬렉션이 발생하는지 예측할 수 있어야 합니다. WeakMap과 WeakSet의 키나 값으로 객체를 사용할 때, 그 객체가 더 이상 참조되지 않는다면 가비지 컬렉션이 발생할 수 있습니다.
- 성 관련 주의 사항으로는 가비지 컬렉션이 더 자주 발생할 수 있으므로, 메모리 사용 패턴을 주의깊게 관찰해야 합니다.

### 한 줄 정리
WeakMap과 WeakSet은 자바스크립트에서 객체의 약한 참조를 관리하고 가비지 컬렉션을 효율적으로 제어할 수 있는 자료구조입니다.