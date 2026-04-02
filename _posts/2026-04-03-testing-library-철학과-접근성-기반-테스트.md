---
title: "[Deep Dive] Testing Library 철학과 접근성 기반 테스트"
date: 2026-04-03 08:12:49 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Testing Library 철학과 접근성 기반 테스트는 사용자와의 상호작용을 중심으로 하는 테스트 방법론입니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 이전 방식의 테스트는 주로 DOM 노드의 존재나 특정 속성 값 등을 확인하는 방식이었습니다. 하지만 사용자의 실제 상호작용을 고려하지 않기 때문에, 버그를 잘못 놓치거나, 또는 실제 사용자 경험과 관련이 없는 코드를 작성하게될 수 있습니다.
- 이전 방식의 한계: DOM 조작을 테스트하는 방식은 복잡하고, 유지보수하기 어렵습니다. 뿐만 아니라, 사용자 인터페이스의 실제 동작에 대해 정확하게 테스트 하지 못합니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Testing Library는 사용자 인터페이스를 렌더링하고, 사용자의 상호작용을 시뮬레이션하는 방식으로 테스트를 진행합니다. 이를 통해 실제 사용자 경험에 대한 테스트를 진행할 수 있습니다.
- ASCII 다이어그램으로 시각화:
```
                 +---------------+
                 |  React 컴포넌트  |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  Testing Library  |
                 |  (사용자 상호작용)  |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  사용자 인터페이스  |
                 |  (렌더링 및 상호작용)  |
                 +---------------+
```

### 코드로 이해하기
```typescript
import { render, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';

const Button = () => {
  const [count, setCount] = React.useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      클릭 수: {count}
    </button>
  );
};

test('button 클릭 시 클릭 수가 증가함', async () => {
  const { getByText } = render(<Button />);
  const button = getByText('클릭 수: 0');

  fireEvent.click(button);
  await waitFor(() => expect(getByText('클릭 수: 1')).toBeInTheDocument());
});
```

```typescript
// 잘못된 사용 예
// getByText를 사용하여 DOM 노드의 존재만 확인
test('button 클릭 시 클릭 수가 증가함', () => {
  const { getByText } = render(<Button />);
  const button = getByText('클릭 수: 0');
  fireEvent.click(button);
  expect(getByText('클릭 수: 1')).toBeInTheDocument(); // 이는 실제 사용자 경험과 다를 수 있음
});

// 올바른 사용 예
// waitFor을 사용하여 실제 사용자 경험과 동일한 타이밍에 테스트 진행
test('button 클릭 시 클릭 수가 증가함', async () => {
  const { getByText } = render(<Button />);
  const button = getByText('클릭 수: 0');
  fireEvent.click(button);
  await waitFor(() => expect(getByText('클릭 수: 1')).toBeInTheDocument());
});
```

### 비교 분석

| 구분 | 기존 DOM 테스트 | Testing Library |
|------|---|---|
| 테스트 방법 | DOM 노드 존재 확인 | 사용자 상호작용 시뮬레이션 |
| 테스트 대상 | DOM 노드 | 사용자 인터페이스 |
| 유지보수도 | 어려움 | 상대적으로 쉬움 |

### 실전 팁
- Best Practice: 사용자 인터페이스의 실제 동작을 테스트하는 것을 우선하도록 합니다. 이는 사용자 경험을 중심으로 테스트를 작성하도록 합니다.
- 흔한 실수와 해결법: 기존 방식의 테스트를 사용하여 DOM 노드의 존재만 확인하는 경우, 이는 실제 사용자 경험과 다를 수 있습니다. 따라서 사용자 인터페이스의 실제 동작을 테스트하기 위한 라이브러리를 선택하세요.
- 성능 관련 주의사항: 실제 사용자 경험을 테스트하는 경우, 테스트 성능이 느려질 수 있습니다. 이를 해결하기 위해 테스트 케이스를 최적화하거나 테스트 라이브러리의 설정을 조정하세요.

### 한 줄 정리
Testing Library 철학과 접근성 기반 테스트는 사용자와의 상호작용을 중심으로 하는 테스트 방법론이며, 사용자 인터페이스의 실제 동작에 대해 테스트를 진행할 수 있습니다.