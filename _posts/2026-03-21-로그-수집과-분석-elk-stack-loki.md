---
title: "[Deep Dive] 로그 수집과 분석 (ELK Stack, Loki)"
date: 2026-03-21 08:09:27 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
로그 수집과 분석은 시스템의 퍼포먼스를 분석하고 문제를 진단하는 데 사용되는 기술이다.

## Deep Dive

### 왜 필요한가?
- 로그 수집과 분석은 시스템의 문제를 진단하고 퍼포먼스를 개선하는 데 사용된다.
- 이전 방식의 한계는 로그 데이터가 너무 많고 복잡하여 수동으로 분석이 어려웠다.

### 내부 동작 원리
- 로그 수집과 분석은 ELK Stack과 Loki 두 가지 주요 기술을 사용한다.
- ELK Stack은 Elasticsearch, Logstash, Kibana로 구성되며, Loki는 Prometheus와 Grafana로 구성된다.
- 로그 데이터는 Logstash를 통해 수집되고, Elasticsearch에서 색인화 된다. 
- Kibana를 통해 로그 데이터를 시각화하고 분석할 수 있다.
- Loki는 로그 데이터를 수집하고, Grafana를 통해 시각화할 수 있다.

```
  +---------------+
  |  로그 발생  |
  +---------------+
           |
           |
           v
  +---------------+
  |  Logstash    |
  |  (로그 수집) |
  +---------------+
           |
           |
           v
  +---------------+
  | Elasticsearch |
  |  (로그 저장)  |
  +---------------+
           |
           |
           v
  +---------------+
  |  Kibana      |
  |  (로그 분석) |
  +---------------+
```

### 코드로 이해하기

```typescript
// Logstash의 input과 output 설정 예
input {
  file {
    path => "/var/log/*"
  }
}
output {
  elasticsearch {
    hosts => "localhost:9200"
    index => "logs"
  }
}
```

```typescript
// 올바른 사용 예: 로그 데이터를 Elasticsearch에 저장
output {
  elasticsearch {
    hosts => "localhost:9200"
    index => "logs"
  }
}
// 잘못된 사용 예: 로그 데이터를 파일에 저장
output {
  file {
    path => "/var/log/output.log"
  }
}
```

### 비교 분석

| 구분 | ELK Stack | Loki |
|------|---|---|
| 로그 수집 | Logstash | Promtail |
| 로그 저장 | Elasticsearch | Object Storage |
| 로그 분석 | Kibana | Grafana |

### 실전 팁
- Best Practice: 로그 데이터를 중앙화하여 관리한다.
- 흔한 실수와 해결법: 로그 데이터가 너무 많아 Elasticsearch에 저장이 안되는 경우, 로그 데이터를 필터링하거나_sampling을 사용하여 데이터 양을 줄일 수 있다.
- 성능 관련 주의사항: Elasticsearch의 퍼포먼스를 개선하기 위해, 데이터를 압축하거나 shard를 나누어 저장할 수 있다.

### 한 줄 정리
로그 수집과 분석을 통해 시스템의 퍼포먼스를 분석하고 문제를 진단할 수 있다.