---
title: "[Deep Dive] Blue-Green vs Canary vs Rolling 배포 전략"
date: 2026-06-04 08:35:11 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Blue-Green, Canary, Rolling 배포 전략은 소프트웨어 배포를 안정적으로 관리하는 방법들입니다.

## Deep Dive

### 왜 필요한가?
- 이러한 배포 전략이 해결하는 문제는 시스템의 가용성과 배포 중단 시간을 최소화하는 것입니다. 이전 방식의 한계는 배포 중 시스템의 가용성이 떨어지는 문제와 배포 실패시 롤백하기 어려운 점이었습니다.

### 내부 동작 원리
- 각 배포 전략의 핵심 메커니즘은 다음과 같습니다.
  - Blue-Green 배포: 두 개의 동일한 환경이 존재하고, 하나는 현환경이고, 또 하나는 준비환경입니다. 준비환경에서 새 버전을 배포하고 테스트 이후에 트래픽을 전환합니다.
  - Canary 배포: 새 버전을 일부 사용자에게만 배포하고, 그 반응을 관찰한 후에 전체 사용자에게 배포합니다.
  - Rolling 배포: 새 버전을적으로 업로드하고, 이전 버전의 서비스를 중단하여 새 버전으로 교체합니다.
  
```
+---------------+    +---------------+
|  Blue Environment  |    |  Green Environment  |
+---------------+    +---------------+
         |                      |
         |  준비                |  준비
         |                      |
         v                      v
+---------------+    +---------------+
|  Blue Service   |    |  Green Service   |
+---------------+    +---------------+
         |                      |
         |  트래픽 전환         |  트래픽 전환
         |                      |
         v                      v
+---------------+    +---------------+
|  Blue Service  |    |  Green Service   |
|  (새 버전)    |    |  (새 버전)     |
+---------------+    +---------------+
```

### 코드로 이해하기
Blue-Green 배포 전략의 간단한 코드 예제는 다음과 같습니다.

```typescript
class BlueGreenDeploy {
    private blueEnvironment: string;
    private greenEnvironment: string;

    constructor(blueEnvironment: string, greenEnvironment: string) {
        this.blueEnvironment = blueEnvironment;
        this.greenEnvironment = greenEnvironment;
    }

    deployNewVersion(newVersion: string) {
        // Green Environment에서 새 버전 배포 및 테스트
        console.log(`배포 환경: ${this.greenEnvironment}`);
        console.log(`새 버전 배포: ${newVersion}`);

        // 트래픽 전환
        console.log("트래픽 전환");
        this.blueEnvironment = this.greenEnvironment;
    }
}
```

### 비교 분석

| 구분 | Blue-Green | Canary | Rolling |
|------|---|---|---|
| 특성1 | 전체 사용자에게 동시에 배포 | 일부 사용자에게 먼저 배포 | 순차적으로 배포 |
| 특성2 | 두 개의 환경 필요 | 일부 사용자 그룹 필요 | 이전 버전의 중단 필요 |
| 특성3 | 빠른 롤백 가능 | 테스트 및 모니터링 필요 | 중단 시간 최소화 |

### 실전 팁
- Best Practice: 배포 전략을 선택할 때는 시스템의 특성과 가용성 요구사항을 고려합니다.
- 흔한 실수와 해결법: 시스템의 복잡성과 가용성 요구사항을 고려하지 않을 경우, 배포 실패나 롤백에 어려움을 겪을 수 있습니다.
- 성능 관련 주의사항: 배포 전략이 시스템의 성능에 영향을 줄 수 있으므로, 성능 테스트와 모니터링을 철저히 수행해야 합니다.

### 한 줄 정리
Blue-Green, Canary, Rolling 배포 전략은 각기 다른 특성을 가지고 있으며, 시스템의 가용성과 배포 중단 시간을 최소화하는 방법입니다.