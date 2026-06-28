---
title: "[Deep Dive] Infrastructure as Code (Terraform, Pulumi)"
date: 2026-06-29 08:26:50 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
인프라스트럭처를 코드로 관리하는 기술입니다.

## Deep Dive

### 왜 필요한가?
- 기존 인프라스트럭처 관리 방식은 수동으로 설정하고 관리해야 하므로 많은 시간과 노력이 필요합니다. 또한 수동으로 관리하다 보니_human이나 중복 설정이 발생할 수 있습니다. 이런 문제를 해결하기 위해 Infrastructure as Code(IaC)가 필요합니다.
- IaC를 사용하면 인프라스트럭처를 코드로 정의하여 버전 관리를 할 수 있고, 자동으로 배포 및 관리를 할 수 있습니다.

### 내부 동작 원리
- Terraform과 Pulumi는 가장 대표적인 IaC 도구입니다. 이 도구들은 인프라스트럭처의 상태를 코드로 정의한 후, 실제 인프라스트럭처와 비교하여 차이점을 파악하고, 자동으로 변경을 적용합니다.
```
+---------------+
|  Config File  |
+---------------+
         |
         |
         v
+---------------+
|  Terraform/Pulumi  |
+---------------+
         |
         |
         v
+---------------+
|  인프라스트럭처  |
+---------------+
```

### 코드로 이해하기
```typescript
// Terraform을 사용한 사례
provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0c94855ba95c71c99"
  instance_type = "t2.micro"
}
```

```typescript
// Pulumi를 사용한 사례
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const instanceType = config.require("instanceType");

const instance = aws.ec2.Instance("example", {
  ami: "ami-0c94855ba95c71c99",
  instanceType: instanceType,
});
```

### 비교 분석

| 구분 | Terraform | Pulumi |
|------|---|---|
| 언어 | HCL | TypeScript, Python, Go |
| 플랫폼 지원 | AWS, GCP, Azure, etc. | AWS, GCP, Azure, etc. |
| 상태 관리 | terraform.tfstate | pulumi.yaml |

### 실전 팁
- Terraform과 Pulumi 모두 버전 관리를 철저히 하세요. 코드의 버전과 인프라스트럭처의 버전을 관리하여 오류를 최소화하세요.
- 상태 파일을 외부에 저장하지 마세요. terraform.tfstate나 pulumi.yaml 파일을 외부에 노출시키지 않도록 주의하세요.
- 작은 단위로 인프라스트럭처를 배포하고, 점진적으로 확장하세요.

### 한 줄 정리
인프라스트럭처를 코드로 관리하여 자동화하고 효율성을 높일 수 있습니다.