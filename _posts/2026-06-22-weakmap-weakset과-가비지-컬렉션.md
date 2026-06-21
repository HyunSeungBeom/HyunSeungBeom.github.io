---
title: "[Deep Dive] WeakMap, WeakSet과 가비지 컬렉션"
date: 2026-06-22 08:32:10 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
WeakMap과 WeakSet은 자바스크립트에서 가비지 컬렉션을 효율적으로 처리할 수 있는 데이터 구조입니다.

## Deep Dive

### 왜 필요한가?
- 기존의 Map과 Set은 키와 값이.gcroots에 의해 참조되기 때문에, 가비지 컬렉션이 이루어질 때 메모리에서 삭제되지 않습니다. WeakMap과 WeakSet은 이러한 문제를 해결합니다.
- 이전 방식에서는 수동으로 키와 값을 삭제해야 했으며, 사용이 불편하고 실수를 유발할 수 있었습니다.

### 내부 동작 원리
- WeakMap과 WeakSet은 키와 값을 약한 참조(Weak Reference)로 처리합니다. 즉,.gcroots에 의해 참조되지 않으며, 가비지 컬렉션이 이루어질 때 자동으로 삭제됩니다.
- 다음은 WeakMap의 내부 동작 원리를 ASCII 다이어그램으로 표현한 예시입니다.
```
  +---------------+
  |  WeakMap    |
  +---------------+
           |
           |
           v
  +---------------+
  |  Key (약한 참조) |
  +---------------+
           |
           |
           v
  +---------------+
  |  Value (약한 참조) |
  +---------------+
           |
           |
           v
  +---------------+
  |  가비지 컬렉션  |
  +---------------+
```

### 코드로 이해하기
```typescript
// WeakMap 사용 예
const weakMap = new WeakMap();
const key = {};
weakMap.set(key, 'value');
console.log(weakMap.get(key)); // 'value'

// 약한 참조로 인한 가비지 컬렉션
key = null;
// 가비지 컬렉션이 발생하면 weakMap에서 키-값 페어가 자동으로 삭제됩니다.
```

```typescript
// 잘못된 사용 예
const weakMap = new WeakMap();
const key = 'string';
weakMap.set(key, 'value'); // TypeError: Invalid value used as weak map key

// 올바른 사용 예
const weakMap = new WeakMap();
const key = {};
weakMap.set(key, 'value'); // 올바른 사용
```

### 비교 분석

| 구분 | Map | Set | WeakMap | WeakSet |
|------|---|---|---|---|
| 키 타입 | | |객체 |객체 |
| 값 타입 | |- | |- |
| 참조 유형 |강한 참조 |강한 참조 |약한 참조 |약한 참조 |
| 가비지 컬렉션 |수동 삭제 필요 |수동 삭제 필요 |자동 삭제 |자동 삭제 |

### 실전 팁
- WeakMap과 WeakSet을 사용할 때는 키와 값을 생성하여 setzenecessity를 명확히 해줘야 합니다.
- 약한 참조로 인해 가비지 컬렉션이 발생할 수 있으므로, 올바른 사용 방법을 이해해야 합니다.
- 성능 관련 주의사항으로는, 약한 참조로 인한 가비지 컬렉션 비용이 추가될 수 있습니다.

### 한 줄 정리
WeakMap과 WeakSet은 약한 참조를 통해 가비지 컬렉션을 효율적으로 처리할 수 있는 데이터 구조입니다.