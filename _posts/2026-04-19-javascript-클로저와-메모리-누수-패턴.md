---
title: "[Deep Dive] JavaScript 클로저와 메모리 누수 패턴"
date: 2026-04-19 08:13:20 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript 클로저와 메모리 누수 패턴은 함수와 변수가 작용을 통해 메모리 누수를 일으키는 상황을 이해하고 해결하는 기술입니다.

## Deep Dive

### 왜 필요한가?
클로저는 JavaScript에서 함수와 함수 스코프로 둘러싸인 변수들의 조합을 말합니다. 클로저는 메모리 누수를 일으킬 수 있습니다. 이전 방식의 한계는 함수의 변수가 함수의 실행이 종료된 후에도 계속 메모리에 남아있을 수 있고, 이로 인해 메모리 누수가 발생할 수 있습니다.

### 내부 동작 원리
클로저의 내부 동작 원리는 함수가 생성될 때 함수 스코프에 포함된 변수를 참조하여 사용할 수 있습니다. ASCII 다이어그램으로 나타내면 다음과 같습니다.
```
+---------------+
|  Outer Func  |
|  +---------+  |
|  |  Var A  |  |
|  +---------+  |
|  |  Inner  |  |
|  |  Func   |  |
|  +---------+  |
+---------------+
```
클로저는 Outer Func의 변수를 참조하여 Inner Func에서 사용할 수 있습니다.

### 코드로 이해하기
```typescript
function outerFunc() {
  let outerVar = 10;

  function innerFunc() {
    console.log(outerVar);
  }

  return innerFunc;
}

const inner = outerFunc();
inner(); // 10
```
위의 코드는 Outer Func에서 Inner Func을 반환하고, Inner Func에서 Outer Func의 변수를 참조하는 클로저의 예입니다.

### 비교 분석

| 구분 | 클로저 | 지역 변수 |
|------|---|---|
| 메모리 참조 | Outer Func의 변수 참조 | 지역 변수만 참조 |
| 메모리 누수 | 가능 | 불가능 |
| 사용법 | 함수 반환 시 사용 | 함수 내부에서 사용 |

### 실전 팁
Best Practice는 클로저를 사용할 때 변수를 참조하는 Inner Func을 반환하고, Outer Func이 종료된 후에도 메모리에 남아있는 변수를 참조하지 않도록 주의해야 합니다. 흔한 실수는 Outer Func의 변수를 Inner Func에서 변경하거나, Outer Func이 종료된 후에도 Inner Func에서 Outer Func의 변수를 참조하는 것입니다. 성능 관련 주의사항은 클로저를 사용할 때 메모리 누수가 발생할 수 있으므로, 변수를 참조하는 Inner Func을 반환하는 것을 주의해야 합니다.

### 한 줄 정리
JavaScript 클로저는 함수와 변수가 작용을 통해 메모리 누수를 일으키는 상황을 이해하고 해결하는 기술입니다.