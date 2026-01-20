---
title: "Frontend Deep Dive 정리"
date: 2026-01-20 12:00:00 +0900
categories: [개발노트]
tags: [JavaScript, React, TypeScript, 성능최적화]
---

> 표면적인 이해를 넘어 "왜?"를 설명할 수 있어야 한다.

---

## 1. 브라우저에 URL을 입력하면 일어나는 일

### 표면적 답변
DNS 조회 → IP 획득 → HTTP 요청 → 응답 → 렌더링

### Deep Dive

```
[사용자 입력] → [URL 파싱] → [HSTS 확인] → [DNS 조회] → [TCP 연결] → [TLS 핸드셰이크]
     → [HTTP 요청] → [서버 처리] → [응답] → [브라우저 렌더링]
```

#### 1) URL 파싱 & HSTS
```
https://www.google.com:443/search?q=hello#section1
  │        │          │     │       │        │
scheme   host       port  path   query   fragment
```
- **HSTS (HTTP Strict Transport Security)**: 브라우저가 내부 목록을 확인해 HTTP → HTTPS 강제 리다이렉트
- Google은 HSTS Preload List에 포함되어 있음

#### 2) DNS 조회 (계층적)
```
1. 브라우저 캐시 (Chrome: chrome://net-internals/#dns)
2. OS 캐시 (/etc/hosts)
3. 라우터 캐시
4. ISP DNS 서버
5. Root DNS → TLD DNS (.com) → Authoritative DNS
```

**DNS 레코드 타입:**
- `A`: IPv4 주소
- `AAAA`: IPv6 주소
- `CNAME`: 별칭 (www → @)
- `MX`: 메일 서버
- `TXT`: SPF, DKIM 등 검증용

#### 3) TCP 3-Way Handshake
```
Client          Server
  │── SYN ────────→│   (seq=x)
  │←── SYN-ACK ────│   (seq=y, ack=x+1)
  │── ACK ────────→│   (ack=y+1)
```

#### 4) TLS 1.3 Handshake (HTTPS)
```
Client                              Server
  │── ClientHello ─────────────────→│  (지원 암호화 스위트, 랜덤값)
  │←── ServerHello + Certificate ───│  (선택된 암호화, 인증서)
  │←── Finished ───────────────────│
  │── Finished ────────────────────→│
  │←──────── 암호화 통신 ──────────→│
```

**TLS 1.3 vs 1.2:**
- 1.3: 1-RTT (또는 0-RTT resume)
- 1.2: 2-RTT

#### 5) HTTP/2 & HTTP/3
```
HTTP/1.1: 요청당 TCP 연결 (또는 Keep-Alive로 재사용)
HTTP/2:   멀티플렉싱 (하나의 TCP 연결에 여러 스트림)
HTTP/3:   QUIC (UDP 기반, 0-RTT 가능)
```

#### 6) 브라우저 렌더링 파이프라인
```
HTML 파싱 → DOM 트리
                    ↘
                      Render Tree → Layout → Paint → Composite
                    ↗
CSS 파싱 → CSSOM 트리
```

**Critical Rendering Path 최적화:**
- CSS는 `<head>`에 (렌더 블로킹)
- JS는 `<body>` 끝에 또는 `defer`/`async`
- Critical CSS 인라인화

**Reflow vs Repaint:**
```javascript
// Reflow 발생 (비용 높음) - 레이아웃 변경
element.style.width = '100px';
element.style.height = '100px';

// Repaint만 발생 (비용 낮음) - 시각적 변경만
element.style.color = 'red';
element.style.backgroundColor = 'blue';

// Composite만 (비용 가장 낮음)
element.style.transform = 'translateX(100px)';
element.style.opacity = '0.5';
```

---

## 2. HTTP 메서드 (GET vs POST 그 이상)

### 표면적 답변
GET은 조회, POST는 생성

### Deep Dive

#### HTTP 메서드의 특성

| 메서드 | 안전(Safe) | 멱등(Idempotent) | 캐시 가능 | 용도 |
|--------|-----------|-----------------|----------|------|
| GET | O | O | O | 리소스 조회 |
| POST | X | X | 조건부 | 리소스 생성, 프로세스 처리 |
| PUT | X | O | X | 리소스 전체 교체 |
| PATCH | X | X | X | 리소스 부분 수정 |
| DELETE | X | O | X | 리소스 삭제 |
| HEAD | O | O | O | 헤더만 조회 |
| OPTIONS | O | O | X | 지원 메서드 확인 (CORS preflight) |

**멱등성(Idempotent)이란?**
```
같은 요청을 여러 번 보내도 결과가 동일

DELETE /users/1  → 첫 번째: 삭제됨, 두 번째: 이미 없음 (결과 동일: user 1 없음)
POST /users      → 첫 번째: user 생성, 두 번째: 또 생성 (결과 다름!)
```

#### GET vs POST 실제 차이

```
GET /search?q=hello&page=1 HTTP/1.1
Host: example.com
```

```
POST /search HTTP/1.1
Host: example.com
Content-Type: application/json

{"q": "hello", "page": 1}
```

| 구분 | GET | POST |
|------|-----|------|
| 데이터 위치 | URL (Query String) | Body |
| 길이 제한 | 브라우저별 2KB~8KB | 서버 설정에 따름 |
| 브라우저 히스토리 | 남음 | 안 남음 |
| 북마크 | 가능 | 불가능 |
| 캐싱 | 기본 캐싱됨 | 기본 캐싱 안됨 |
| 인코딩 | URL 인코딩만 | 다양한 인코딩 |

**보안 관점:**
```
GET은 민감 정보에 부적합
GET /login?username=admin&password=1234  → URL에 노출, 로그에 기록

POST도 HTTPS 없이는 안전하지 않음
Body도 평문 전송됨 → 반드시 HTTPS 사용
```

---

## 3. JavaScript 실행 컨텍스트 & 클로저

### 표면적 답변
렉시컬 환경은 코드가 선언된 환경

### Deep Dive

#### 실행 컨텍스트 구조

```javascript
ExecutionContext = {
  LexicalEnvironment: {
    EnvironmentRecord: { /* 변수, 함수 선언 */ },
    outer: /* 외부 렉시컬 환경 참조 */
  },
  VariableEnvironment: { /* var 선언 */ },
  ThisBinding: /* this 값 */
}
```

#### 호이스팅의 진짜 원리

```javascript
console.log(a); // undefined (var: 선언 + 초기화)
console.log(b); // ReferenceError (let: 선언만, TDZ)
console.log(c); // ReferenceError (const: 선언만, TDZ)

var a = 1;
let b = 2;
const c = 3;
```

**TDZ (Temporal Dead Zone):**
```javascript
// TDZ 시작 ─────────────────┐
console.log(x); // ReferenceError │
let x = 10;     // TDZ 끝 ────────┘
console.log(x); // 10
```

#### 클로저 (Closure)

```javascript
function outer() {
  let count = 0;  // 자유 변수 (Free Variable)

  return function inner() {
    return ++count;
  };
}

const counter = outer();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3

// outer()의 실행 컨텍스트는 종료됐지만
// inner()가 outer의 LexicalEnvironment를 참조하고 있어
// count 변수가 가비지 컬렉션되지 않음
```

**실전 활용: Private 변수**
```javascript
function createBankAccount(initialBalance) {
  let balance = initialBalance; // private

  return {
    deposit(amount) {
      balance += amount;
      return balance;
    },
    withdraw(amount) {
      if (balance >= amount) {
        balance -= amount;
        return balance;
      }
      throw new Error('잔액 부족');
    },
    getBalance() {
      return balance;
    }
  };
}

const account = createBankAccount(1000);
account.deposit(500);  // 1500
account.balance;       // undefined (접근 불가)
```

**클로저 주의점: 루프 문제**
```javascript
// 문제
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 출력: 3, 3, 3 (var는 함수 스코프)

// 해결 1: let (블록 스코프)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 출력: 0, 1, 2

// 해결 2: IIFE로 클로저 생성
for (var i = 0; i < 3; i++) {
  ((j) => {
    setTimeout(() => console.log(j), 100);
  })(i);
}
```

---

## 4. this 바인딩

### 표면적 답변
this는 자신이 속한 객체를 가리킴

### Deep Dive

#### this 바인딩 규칙 (우선순위 순)

```javascript
// 1. new 바인딩 (최우선)
function Person(name) {
  this.name = name;
}
const p = new Person('Kim'); // this → 새 객체

// 2. 명시적 바인딩 (call, apply, bind)
function greet() {
  console.log(this.name);
}
const obj = { name: 'Lee' };
greet.call(obj);   // 'Lee'
greet.apply(obj);  // 'Lee'
const bound = greet.bind(obj);
bound();           // 'Lee'

// 3. 암시적 바인딩 (메서드 호출)
const user = {
  name: 'Park',
  greet() {
    console.log(this.name);
  }
};
user.greet(); // 'Park' (this → user)

// 4. 기본 바인딩
function foo() {
  console.log(this);
}
foo(); // window (strict mode: undefined)
```

#### 암시적 바인딩 손실

```javascript
const user = {
  name: 'Kim',
  greet() {
    console.log(this.name);
  }
};

const greetFn = user.greet;
greetFn(); // undefined (this → window)

// 콜백에서 자주 발생
setTimeout(user.greet, 100); // undefined

// 해결: bind
setTimeout(user.greet.bind(user), 100); // 'Kim'
```

#### 화살표 함수의 this

```javascript
// 화살표 함수는 자체 this가 없음 → 렉시컬 this (상위 스코프의 this)
const obj = {
  name: 'Kim',

  // 일반 함수: 호출 시점에 this 결정
  regularMethod() {
    setTimeout(function() {
      console.log(this.name); // undefined (this → window)
    }, 100);
  },

  // 화살표 함수: 선언 시점의 상위 스코프 this
  arrowMethod() {
    setTimeout(() => {
      console.log(this.name); // 'Kim' (this → obj)
    }, 100);
  }
};
```

**화살표 함수 주의점:**
```javascript
// 메서드로 사용하면 안됨
const obj = {
  name: 'Kim',
  greet: () => {
    console.log(this.name); // undefined (this → window)
  }
};

// 생성자로 사용 불가
const Person = (name) => {
  this.name = name;
};
new Person('Kim'); // TypeError

// addEventListener에서 주의
button.addEventListener('click', () => {
  console.log(this); // window (의도: button)
});

button.addEventListener('click', function() {
  console.log(this); // button
});
```

---

## 5. 이벤트 루프 & 비동기

### 표면적 답변
async/await는 Promise를 더 쉽게 사용하는 문법

### Deep Dive

#### JavaScript 런타임 구조

```
┌─────────────────────────────────────────────────────────┐
│                    JavaScript Engine                     │
│  ┌─────────────┐  ┌──────────────────────────────────┐  │
│  │  Call Stack │  │           Heap (Memory)          │  │
│  │             │  │                                  │  │
│  │ [함수 실행] │  │    [객체, 변수 저장]             │  │
│  └─────────────┘  └──────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                    Event Loop
                          │
┌─────────────────────────────────────────────────────────┐
│                      Web APIs                            │
│   setTimeout, fetch, DOM Events, XMLHttpRequest         │
└─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌─────────────────┐              ┌─────────────────────┐
│  Macrotask Queue │              │  Microtask Queue    │
│  (Task Queue)    │              │                     │
│                  │              │                     │
│ - setTimeout     │              │ - Promise.then      │
│ - setInterval    │              │ - queueMicrotask    │
│ - I/O            │              │ - MutationObserver  │
│ - UI rendering   │              │                     │
└─────────────────┘              └─────────────────────┘
```

#### 이벤트 루프 실행 순서

```javascript
console.log('1');

setTimeout(() => console.log('2'), 0);

Promise.resolve()
  .then(() => console.log('3'))
  .then(() => console.log('4'));

console.log('5');

// 출력: 1, 5, 3, 4, 2
```

**실행 과정:**
```
1. Call Stack: console.log('1') → 출력 "1"
2. Call Stack: setTimeout → Web API로 이동 → Macrotask Queue에 콜백 추가
3. Call Stack: Promise.resolve().then() → Microtask Queue에 콜백 추가
4. Call Stack: console.log('5') → 출력 "5"
5. Call Stack 비어있음 → Microtask Queue 처리
   - console.log('3') → 출력 "3"
   - console.log('4') → 출력 "4"
6. Microtask Queue 비어있음 → Macrotask Queue 처리
   - console.log('2') → 출력 "2"
```

#### async/await 동작 원리

```javascript
async function foo() {
  console.log('1');
  await bar();        // 여기서 Promise가 resolve될 때까지 대기
  console.log('3');   // 이 부분은 Microtask Queue로
}

async function bar() {
  console.log('2');
}

foo();
console.log('4');

// 출력: 1, 2, 4, 3
```

**await 이후 코드는 .then()과 동일:**
```javascript
// async/await
async function example() {
  const result = await fetch('/api');
  console.log(result);
}

// 동등한 Promise
function example() {
  return fetch('/api').then(result => {
    console.log(result);
  });
}
```

---

## 6. React 렌더링 최적화

### 표면적 답변
useMemo, useCallback, React.memo로 최적화

### Deep Dive

#### React 렌더링 프로세스

```
State/Props 변경
       ↓
Render Phase (순수, 중단 가능)
  - 컴포넌트 함수 호출
  - Virtual DOM 생성
  - Diffing (Reconciliation)
       ↓
Commit Phase (부수효과, 중단 불가)
  - DOM 업데이트
  - useLayoutEffect 실행
  - useEffect 실행
```

#### 리렌더링이 발생하는 경우

```javascript
// 1. State 변경
const [count, setCount] = useState(0);
setCount(1); // 리렌더링

// 2. Props 변경
<Child value={count} /> // count 변경 시 Child 리렌더링

// 3. 부모 컴포넌트 리렌더링
function Parent() {
  const [count, setCount] = useState(0);
  return <Child />; // Parent 리렌더링 → Child도 리렌더링 (props 안 바뀌어도!)
}

// 4. Context 값 변경
const ThemeContext = createContext();
// Provider의 value 변경 → 모든 Consumer 리렌더링
```

#### React.memo 제대로 이해하기

```javascript
// React.memo: props가 같으면 리렌더링 스킵
const Child = React.memo(({ value, onClick }) => {
  console.log('Child render');
  return <button onClick={onClick}>{value}</button>;
});

function Parent() {
  const [count, setCount] = useState(0);

  // 매 렌더링마다 새 함수 생성 → Child 리렌더링
  const handleClick = () => console.log('clicked');

  // useCallback으로 함수 메모이제이션
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return <Child value="hello" onClick={handleClick} />;
}
```

#### useMemo vs useCallback vs React.memo

```javascript
// useMemo: 값을 메모이제이션
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// useCallback: 함수를 메모이제이션 (useMemo의 함수 버전)
const memoizedFn = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// 사실 useCallback은 useMemo의 syntactic sugar
const memoizedFn = useMemo(() => {
  return () => doSomething(a, b);
}, [a, b]);

// React.memo: 컴포넌트를 메모이제이션
const MemoizedComponent = React.memo(Component);
```

---

## 7. Virtual DOM & Reconciliation

### 표면적 답변
Virtual DOM으로 효율적으로 DOM 업데이트

### Deep Dive

#### Virtual DOM이란?

```javascript
// React Element (Virtual DOM Node)
const element = {
  type: 'div',
  props: {
    className: 'container',
    children: [
      {
        type: 'h1',
        props: { children: 'Hello' }
      },
      {
        type: 'p',
        props: { children: 'World' }
      }
    ]
  }
};

// JSX는 이것의 문법 설탕
<div className="container">
  <h1>Hello</h1>
  <p>World</p>
</div>
```

#### Diffing 알고리즘

```javascript
// 1. 다른 타입의 엘리먼트 → 트리 전체 교체
// Before
<div><Counter /></div>
// After
<span><Counter /></span>
// → div 언마운트, span 마운트, Counter 상태 초기화

// 2. 같은 타입의 DOM 엘리먼트 → 속성만 업데이트
// Before
<div className="before" title="stuff" />
// After
<div className="after" title="stuff" />
// → className만 변경

// 3. 같은 타입의 컴포넌트 → 인스턴스 유지, props 업데이트
// Before
<Counter count={1} />
// After
<Counter count={2} />
// → 같은 인스턴스, componentDidUpdate 호출
```

#### Key의 중요성

```javascript
// key 없이 리스트 렌더링
<ul>
  {items.map(item => <li>{item.name}</li>)}
</ul>
// 맨 앞에 아이템 추가 시 → 모든 li 업데이트

// index를 key로 사용
<ul>
  {items.map((item, index) => <li key={index}>{item.name}</li>)}
</ul>
// 순서 변경 시 → 잘못된 컴포넌트 매칭, 상태 꼬임

// 고유 ID를 key로 사용
<ul>
  {items.map(item => <li key={item.id}>{item.name}</li>)}
</ul>
// 정확한 매칭 → 최소한의 DOM 조작
```

---

## 8. useEffect vs useLayoutEffect

### 표면적 답변
useEffect는 비동기, useLayoutEffect는 동기

### Deep Dive

#### 실행 시점

```
브라우저 렌더링 타임라인:
──────────────────────────────────────────────────────────→
  │          │              │            │
  │          │              │            └─ useEffect (비동기, paint 후)
  │          │              │
  │          │              └─ Paint (화면에 그리기)
  │          │
  │          └─ useLayoutEffect (동기, paint 전)
  │
  └─ DOM 업데이트 (Commit)
```

#### 시각적 차이

{% raw %}
```javascript
// useEffect: 깜빡임 발생 가능
function FlickerComponent() {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    setWidth(100);  // paint 후 실행 → 0 → 100 깜빡임
  }, []);

  return <div style={{ width: `${width}px` }} />;
}

// useLayoutEffect: 깜빡임 없음
function NoFlickerComponent() {
  const [width, setWidth] = useState(0);

  useLayoutEffect(() => {
    setWidth(100);  // paint 전 실행 → 바로 100
  }, []);

  return <div style={{ width: `${width}px` }} />;
}
```
{% endraw %}

---

## 9. 깊은 복사 vs 얕은 복사

### 표면적 답변
얕은 복사는 주소 복사, 깊은 복사는 완전 복사

### Deep Dive

#### 메모리 구조 이해

```javascript
// Primitive (원시값) - Stack에 값 저장
let a = 1;
let b = a;    // 값 복사
b = 2;
console.log(a); // 1 (영향 없음)

// Reference (참조값) - Heap에 값, Stack에 주소 저장
let obj1 = { name: 'Kim' };
let obj2 = obj1;  // 주소 복사
obj2.name = 'Lee';
console.log(obj1.name); // 'Lee' (영향 있음!)
```

```
Stack                     Heap
┌─────────────┐          ┌─────────────────┐
│ a: 1        │          │                 │
│ b: 2        │          │                 │
│             │          │                 │
│ obj1: 0x001 │────────→ │ { name: 'Lee' } │
│ obj2: 0x001 │────────→ │                 │
└─────────────┘          └─────────────────┘
```

#### 깊은 복사 (Deep Copy)

```javascript
const original = {
  name: 'Kim',
  address: { city: 'Seoul' },
  hobbies: ['reading', 'coding']
};

// 방법 1: JSON (한계 있음)
const copy1 = JSON.parse(JSON.stringify(original));
// 함수, undefined, Symbol, 순환 참조 처리 못함

// 방법 2: structuredClone (Modern)
const copy2 = structuredClone(original);
// Date, Map, Set, ArrayBuffer 등 지원

// 방법 3: Lodash
import { cloneDeep } from 'lodash';
const copy3 = cloneDeep(original);
```

---

## 10. 이벤트 버블링 & 캡처링

### 표면적 답변
버블링은 자식→부모, 캡처링은 부모→자식

### Deep Dive

#### 이벤트 흐름 3단계

```
            ┌───────────────────────────┐
            │         window            │
            │   ┌───────────────────┐   │
            │   │      document     │   │
            │   │   ┌───────────┐   │   │
        1   │   │   │   body    │   │   │   3
  Capturing │   │   │  ┌─────┐  │   │   │  Bubbling
     ↓      │   │   │  │ div │  │   │   │     ↑
            │   │   │  │┌───┐│  │   │   │
            │   │   │  ││btn││←─│───│───│─── Event Target
            │   │   │  │└───┘│  │   │   │      (2)
            │   │   │  └─────┘  │   │   │
            │   │   └───────────┘   │   │
            │   └───────────────────┘   │
            └───────────────────────────┘
```

#### 이벤트 위임 (Event Delegation)

```javascript
// 각 요소에 이벤트 리스너 (비효율)
document.querySelectorAll('li').forEach(li => {
  li.addEventListener('click', handleClick);
});

// 이벤트 위임 (효율적)
document.querySelector('ul').addEventListener('click', (e) => {
  const li = e.target.closest('li');
  if (!li) return;
  handleClick(li);
});
```

---

## 11. TypeScript 타입 시스템

### 표면적 답변
타입을 명시해서 안전하게 코딩

### Deep Dive

#### 구조적 타이핑 (Structural Typing)

```typescript
// TypeScript는 구조로 타입 호환성 판단 (Duck Typing)
interface Point {
  x: number;
  y: number;
}

// Point를 요구하는 곳에 더 많은 속성을 가진 객체도 OK
function logPoint(p: Point) {
  console.log(`${p.x}, ${p.y}`);
}

const point3D = { x: 1, y: 2, z: 3 };
logPoint(point3D); // OK!

// 하지만 객체 리터럴은 초과 속성 검사 (Excess Property Check)
logPoint({ x: 1, y: 2, z: 3 }); // Error!
```

#### 고급 타입 패턴

```typescript
// 1. Template Literal Types
type EventName = `on${Capitalize<'click' | 'focus' | 'blur'>}`;
// 'onClick' | 'onFocus' | 'onBlur'

// 2. Conditional Types + infer
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type Result = UnwrapPromise<Promise<string>>; // string

// 3. Mapped Types
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};
```

---

## 12. 웹 성능 최적화

### Core Web Vitals

```
LCP (Largest Contentful Paint): 2.5초 이내
  - 가장 큰 콘텐츠가 보이는 시간
  - 최적화: 이미지 최적화, 서버 응답 시간, CSS 블로킹 제거

FID (First Input Delay): 100ms 이내
  - 첫 입력에 대한 응답 시간
  - 최적화: JS 실행 시간 단축, 코드 분할

CLS (Cumulative Layout Shift): 0.1 이하
  - 예상치 못한 레이아웃 이동
  - 최적화: 이미지 크기 지정, 동적 콘텐츠 공간 확보
```

### 최적화 기법

```javascript
// 1. 코드 분할
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// 2. 디바운스 & 쓰로틀
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// 3. 가상화 (대용량 리스트)
import { FixedSizeList } from 'react-window';
```
