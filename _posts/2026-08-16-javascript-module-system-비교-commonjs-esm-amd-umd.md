---
title: "[Deep Dive] JavaScript Module System 비교 (CommonJS, ESM, AMD, UMD)"
date: 2026-08-16 08:19:26 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
JavaScript Module System은 여러가지 방식으로 구성될 수 있으며, 각각의 특징과 장단점을 비교분석하는 것이 중요하다.

## Deep Dive

### 왜 필요한가?
JavaScript Module System은 프로젝트의 규모가 커질수록 코드를 관리하고 유지보수하는 것에 대한 필요성이 어난다. 이전에는 스크립트 태그를 사용하여 전체 페이지에 대해 코드를 로딩하는 방식이 일반적이었으나, 이는 성능과 관리의 문제를 야기했다. Module System은 이러한 문제를 해결하기 위해 등장했다.

### 내부 동작 원리
JavaScript Module System은 각각의 모듈이 독립적인 환경에서 실행되고, 필요할 때 다른 모듈을 임포트하여 사용할 수 있다. 이러한 동작 원리는 모듈을 로딩하고, 의존성을 관리하는 방식에 따라 달라진다.
```
          +---------------+
          |  Module A   |
          +---------------+
                  |
                  | Import
                  v
          +---------------+
          |  Module B   |
          +---------------+
                  |
                  | Import
                  v
          +---------------+
          |  Module C   |
          +---------------+
```
이 다이어그램은 Module A가 Module B를 임포트하고, Module B가 Module C를 임포트하는 과정을 보여준다.

### 코드로 이해하기

```javascript
// CommonJS
const moduleB = require('./moduleB');
moduleB.function();

// ESM
import { function } from './moduleB.js';
function();
```

```javascript
// 잘못된 사용 예: CommonJS와 ESM을 함께 사용하는 경우
const moduleB = require('./moduleB'); // CommonJS
import { function } from './moduleB.js'; // ESM

// 올바른 사용 예: 한 가지 Module System만 사용하는 경우
import { function } from './moduleB.js'; // ESM
function();
```

### 비교 분석

| 구분 | CommonJS | ESM | AMD | UMD |
|------|----------|-----|-----|-----|
| 로딩 방식 | 동적 로딩 | 정적 로딩 | 동적 로딩 | 동적/정적 로딩 |
| 사용 범위 | Node.js | 브라우저/Node.js | 브라우저 | 브라우저/Node.js |
| 모듈 종속성 | 런타임에 결정 | 컴파일 타임에 결정 | 런타임에 결정 | 런타임에 결정 |

### 실전 팁
- 프로젝트의 규모와 성격에 따라 적절한 Module System을 선택하자.
- ESM을 사용하는 경우, 브라우저의 호환성을 고려해야 한다.
- Module System을 혼용하는 경우, 모듈의 종속성을 명확하게 qun해야 한다.

### 한 줄 정리
JavaScript Module System은 프로젝트의 규모와 성격에 따라 다양한 방식으로 구성될 수 있으며, 각각의 특징과 장단점을 비교분석하여 적절한 선택을 하는 것이 중요하다.