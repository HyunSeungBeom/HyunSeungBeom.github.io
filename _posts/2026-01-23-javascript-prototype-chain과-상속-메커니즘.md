---
title: "[Deep Dive] JavaScript Prototype Chain과 상속 메커니즘"
date: 2026-01-23 23:06:30 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript Prototype Chain과 상속 메커니즘은 객체 지향 프로그래밍에서 객체 간의 관계를 정의하고 재사용성을 높이는 데 사용된다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: JavaScript는 프로토타입 기반의 객체 지향 언어로, 프로토타입을 사용하여 객체 간의 관계를 정의할 수 있다. 하지만, 이러한 관계를 사용하여 객체를 생성하고 수정하는 방법인 상속 메커니즘이 필요하다.
- 이전 방식의 한계: 전통적인 클래스 기반의 객체 지향 언어에서는 클래스와 상속을 사용하여 객체 간의 관계를 정의하지만, JavaScript에서는 프로토타입을 사용하여 객체를 생성하고 수정할 수 있다.

### 내부 동작 원리
- 핵심 메커니즘 설명: 프로토타입 체인은 한 객체가 다른 객체를 상속받을 때, 상속받은 객체의 프로퍼티와 메소드를 자신의 프로퍼티와 메소드처럼 사용할 수 있게 한다. 이러한 관계는prototype 프로퍼티를 사용하여 설정되며, 프로토타입 체인은 여러 개의 객체를 연결하여 구성된다.
- ASCII 다이어그램으로 시각화:
```
+---------------+
|  Object      |
+---------------+
       |
       |
       v
+---------------+
|  Person      |
|  (prototype) |
+---------------+
       |
       |
       v
+---------------+
|  Employee    |
|  (prototype) |
+---------------+
       |
       |
       v
+---------------+
|  Manager     |
|  (prototype) |
+---------------+
```

### 코드로 이해하기

```typescript
// Person 클래스
class Person {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

// Employee 클래스
class Employee extends Person {
  department: string;
  constructor(name: string, department: string) {
    super(name);
    this.department = department;
  }
}

// Manager 클래스
class Manager extends Employee {
  team: string;
  constructor(name: string, department: string, team: string) {
    super(name, department);
    this.team = team;
  }
}

// 인스턴스 생성
const manager = new Manager('John Doe', 'Sales', 'A-Team');
console.log(manager.name); // John Doe
console.log(manager.department); // Sales
console.log(manager.team); // A-Team
```

```typescript
// 잘못된 사용 예 (❌)
class Person {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

class Employee {
  department: string;
  constructor(department: string) {
    this.department = department;
  }
}

const employee = new Employee('Sales');
console.log(employee.name); // undefined

// 올바른 사용 예 (✅)
class Person {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

class Employee extends Person {
  department: string;
  constructor(name: string, department: string) {
    super(name);
    this.department = department;
  }
}

const employee = new Employee('John Doe', 'Sales');
console.log(employee.name); // John Doe
```

### 비교 분석

| 구분 | 상속 | 컴포지션 |
|------|---|---|
| 특성1 | 프로토타입 체인을 사용하여 객체 간의 관계를 정의 | 객체를 다른 객체에 포함시켜서 관계를 정의 |
| 특성2 | 클래스와 인스턴스 사이의 관계를 정의 | 객체와 객체 사이의 관계를 정의 |

### 실전 팁
- Best Practice: 상속과 컴포지션을 적절히 사용하여 객체 간의 관계를 정의하라.
- 흔한 실수와 해결법: 프로토타입 체인을 잘못 설정하여 객체 간의 관계가 정의되지 않는 경우, `prototype` 프로퍼티를 사용하여 프로토타입 체인을 설정하라.
- 성능 관련 주의사항: 프로토타입 체인이 깊을 경우, 객체를 생성하고 수정하는 데 시간이 걸릴 수 있으니, 성능을 고려하여 설계하라.

### 한 줄 정리
JavaScript의 프로토타입 체인과 상속 메커니즘을 사용하여 객체 간의 관계를 정의하고, 객체를 생성하고 수정하는 데 사용할 수 있다.