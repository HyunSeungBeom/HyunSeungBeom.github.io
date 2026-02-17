---
title: "[Deep Dive] Infrastructure as Code (Terraform, Pulumi)"
date: 2026-02-18 08:10:03 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
인프라스트럭처를 코드로 관리하는 기술인 Infrastructure as Code(IaC)는 Terraform, Pulumi 등의 도구를 통해 인프라 설정을 자동화하고 버전 관리를 합니다.

## Deep Dive

### 왜 필요한가?
- 인프라스트럭처를 수동으로 설정하는 방식은 시간이 오래 걸리고 오류가 발생하기 쉽습니다. 따라서 자동화 도구가 필요합니다. 이전에는 인프라스트럭처를 설정하기 위해 쉘 스크립트나 맨눈으로 설정했습니다. 하지만 이러한 방식에는 단점이 있습니다. 예를 들어, 설정파일이 관리되지 않거나 설정 항목이 누락될 가능성이며, 이를 찾고 고치기 위해 많은 시간이 소요됩니다.

### 내부 동작 원리
- Terraform과 Pulumi는 인프라스트럭처 설정 파일을 해석하여 클라우드 제공 업체에 설정을 적용합니다. 다음은 Terraform의 동작 과정을 보여주는 ASCII 다이어그램입니다.
```
                                  +---------------+
                                  |  설정 파일  |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  | Terraform    |
                                  |  (설정 파일  |
                                  |  해석 및 적용)|
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  클라우드 제공  |
                                  |  업체 API      |
                                  +---------------+
                                            |
                                            |
                                            v
                                  +---------------+
                                  |  인프라스트럭처 |
                                  |  (설정 적용)    |
                                  +---------------+
```

### 코드로 이해하기

```typescript
// Terraform 설정 파일 예시
provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"
}
```

```typescript
// Pulumi 설정 파일 예시
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const instanceType = config.require("instanceType");

const server = aws.ec2.Instance("server", {
  ami: "ami-0c94855ba95c71c99",
  instanceType: instanceType,
});
```

### 비교 분석

| 구분 | Terraform | Pulumi | CloudFormation |
|------|-------------|---------|----------------|
| 설정 파일 언어 | HCL | 일반 프로그래밍 언어 (예: TypeScript) | JSON/YAML |
| 클라우드 제공 업체 지원 범위 | | | AWS만 |
| 상태 관리 | terraform.tfstate | 자동 관리 | CloudFormation 스택 |

### 실전 팁
- 설정 파일을 버전 관리 시스템에 저장하여 변경 내역을 추적합니다.
- 설정 파일을화하여 재사용성을 높입니다.
- 상태 관리를 철저히 하여 인프라스트럭처의 일관성을 유지합니다.

### 한 줄 정리
인프라스트럭처를 코드로 관리하는 것은 자동화를 통해 인프라스트럭처 관리를 효율화하고, 버전 관리를 통해 안정성을 향상시키는 것입니다.