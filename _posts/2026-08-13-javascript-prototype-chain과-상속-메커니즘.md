---
title: "[Deep Dive] JavaScript Prototype Chain과 상속 메커니즘"
date: 2026-08-13 08:40:10 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript의 Prototype Chain과 상속 메커니즘은 객체의 속성과 메소드를 다른 객체와 공유할 수 있도록 해주는 핵심 개념이다.

## Deep Dive

### 왜 필요한가?
- JavaScript의 Prototype Chain과 상속 메커니즘은 객체 지향 프로그래밍의 기본 개념인 상속을 구현하기 위해 필요하다. 이전 방식의 한계는 코드의 중복과 유지 보수가 어려웠다. Prototype Chain과 상속 메커니즘을 사용하면 코드의 재사용성을하고 유지 보수를 쉽게 한다.

### 내부 동작 원리
- JavaScript의 Prototype Chain은 객체의 속성과 메소드를 다른 객체와 공유할 수 있도록 해주는 체인이다. 각 객체에는 프로토 프로퍼가 있다. 이 프로퍼티는 객체의 프로토타입을 참조한다. 프로토은 또 다른 객체의 프로퍼티를 참조할 수 있다. 이러한 체인을 통해 객체는 자신의 프로퍼티와 메소드에 접근할 수 있을 뿐만 아니라, 프로토타입 객체의 프로퍼티와 메소드에도 접근할 수 있다.
```
+---------------+
|  Object     |
+---------------+
|  prototype  |
+---------------+
       |
       |
       v
+---------------+
|  Prototype  |
+---------------+
|  prototype  |
+---------------+
       |
       |
       v
+---------------+
|  Root Object|
+---------------+
```

### 코드로 이해하기
```typescript
class Animal {
  sound() {
    console.log('사운드');
  }
}

class Dog extends Animal {
  sound() {
    console.log('멍멍');
  }
}

const dog = new Dog();
dog.sound(); // 멍멍
```

```typescript
// 잘못된 사용 예
class Animal {
  sound() {
    console.log('사운드');
  }
}

class Dog {
  sound() {
    console.log('멍멍');
  }
}

const dog = new Dog();
// Dog는 Animal을 상속하지 않았으므로 Animal의 메소드에 접근할 수 없다.

// 올바른 사용 예
class Animal {
  sound() {
    console.log('사운드');
  }
}

class Dog extends Animal {
  sound() {
    console.log('멍멍');
  }
}

const dog = new Dog();
dog.sound(); // 멍멍
```

### 비교 분석
| 구분 | 프로토 체인 | 상속 |
|------|---|---|
| 특성1 | 객체의 속성과 메소드를 다른 객체와 공유 | 코드의 재사용성을 높여준다 |
| 특성2 | 프로토 프로퍼티를 통해 체인이 형성된다 | 객체 지향 프로그래밍의 기본 개념 |

### 실전 팁
- 프로토 체인을 사용할 때는 프로퍼티와 메소드의 이름을 중복되지 않도록 주의한다.
- 상속을 사용할 때는 부모 클래스와 자식 클래스의 관계를 명확히 한다.
- 프로토 체인과 상속을 혼용하여 사용할 때는 프로퍼티와 메소드의 접근를 주의한다.

### 한 줄 정리
JavaScript의 Prototype Chain과 상속 메커니즘은 객체 지향 프로그래밍의 기본 개념인 상속을 구현하기 위해 필요하다.