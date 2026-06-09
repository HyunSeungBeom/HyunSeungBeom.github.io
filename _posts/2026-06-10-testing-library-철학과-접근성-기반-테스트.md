---
title: "[Deep Dive] Testing Library 철학과 접근성 기반 테스트"
date: 2026-06-10 08:31:09 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Testing Library 철학과 접근성 기반 테스트는 사용자에게 친화적인 사용자 인터페이스를 제공하는 방법으로, 사용자의 관점에서 테스트를 작성하고 웹의 본질에 대한 이해를 높이는 데 중점을 둔다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 이전의 테스트 방식은 DOM을 직접 조작하여 테스트를 작성하는 방식을 사용했지만, 이 방식은 사용자와의 상호작용을 고려하지 못한다. Testing Library는 사용자가 실제로 어떻게 상호작용하는지 고려하여 테스트를 작성한다.
- 이전 방식의 한계: 이전 방식은 DOM의 구조적인 변화를 고려하여 테스트를 작성했지만, 사용자의 실제 행동을 고려하지 못해 테스트의 신뢰도를 낮추었다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Testing Library는 사용자의 행동을 시뮬레이션하여 테스트를 작성한다. 사용자는 버튼을 클릭하거나 입력 필드에 값을 입력하는 등 다양한 행동을 할 수 있다.
- ASCII 다이어그램으로 시각화:
```
  +---------------+
  |  사용자 행동  |
  +---------------+
           |
           |
           v
  +---------------+
  | Testing Library|
  +---------------+
           |
           |
           v
  +---------------+
  |  실제 결과 확인  |
  +---------------+
```

### 코드로 이해하기

```typescript
// 예: 버튼 클릭 시 메시지 표시
import { render, fireEvent, screen } from '@testing-library/react';

test('버튼 클릭 시 메시지 표시', () => {
  const { getByText } = render(<Button />);
  const button = getByText('클릭');
  const message = screen.queryByText('메시지');

  expect(message).toBeNull();

  fireEvent.click(button);

  expect(screen.getByText('메시지')).toBeInTheDocument();
});
```

```typescript
// 잘못된 사용 예
// 오직 DOM의 구조만을 테스트한다.
test('버튼이 표시되는지', () => {
  const { container } = render(<Button />);
  const button = container.querySelector('button');

  expect(button).toBeInTheDocument();
});

// 올바른 사용 예
// 사용자의 행동을 고려하여 테스트한다.
test('버튼 클릭 시 메시지 표시', () => {
  const { getByText } = render(<Button />);
  const button = getByText('클릭');
  const message = screen.queryByText('메시지');

  expect(message).toBeNull();

  fireEvent.click(button);

  expect(screen.getByText('메시지')).toBeInTheDocument();
});
```

### 비교 분석

| 구분 | DOM 직접 조작 | Testing Library |
|------|---|---|
| 사용자 행동 고려 | X | O |
| 실제 결과 확인 | X | O |
| 코드의 가독성 | 낮음 | 높음 |

### 실전 팁
- Best Practice: 사용자의 실제 행동을 고려하여 테스트를 작성한다.
- 흔한 실수와 해결법: DOM의 구조만을 테스트하는 경우, 사용자의 행동을 고려하여 테스트를 다시 작성한다.
- 성능 관련 주의사항: 사용자의 행동을 시뮬레이션하는 경우, 성능에을 주지 않도록 주의한다.

### 한 줄 정리
Testing Library는 사용자의 실제 행동을 고려하여 테스트를 작성하여, 웹의 본질에 대한 이해를 높이고 사용자에게 친화적인 사용자 인터페이스를 제공하는 데 도움이 된다.