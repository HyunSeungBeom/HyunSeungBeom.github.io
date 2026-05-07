---
title: "[Deep Dive] 로그 수집과 분석 (ELK Stack, Loki)"
date: 2026-05-08 08:21:21 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
로그 수집과 분석은 시스템의 상태를 파악하고 문제를 진단하는 데 중요한 역할을 하는데 ELK Stack과 Loki는 이러한 기능을 제공합니다.

## Deep Dive

### 왜 필요한가?
- 시스템의 상태를 파악하고 문제를 진단하기 위해 로그를 수집하고 분석하는 기술이 필요합니다.
- 이전에 로그 파일을 직접 확인하거나, 일부 툴을 사용하여 로그를 수집하고 분석했지만, 이러한 방식은 제한적이고 불편했습니다.

### 내부 동작 원리
- 로그 수집: ELK Stack의 Logstash, Loki의 Promtail과 같은 에이전트가 로그 파일을 읽어들여 처리합니다.
- 로그 분석: ELK Stack의 Elasticsearch, Loki의 Grafana와 같은 도구를 사용하여 로그를 분석하고 시각화합니다.
```
                +---------------+
                |  로그 파일  |
                +---------------+
                         |
                         |
                         v
                +---------------+
                | Logstash/Promtail|
                |  (에이전트)      |
                +---------------+
                         |
                         |
                         v
                +---------------+
                | Elasticsearch  |
                |  (로그 저장소) |
                +---------------+
                         |
                         |
                         v
                +---------------+
                |  Kibana/Grafana |
                |  (로그 분석 도구) |
                +---------------+
```

### 코드로 이해하기
```typescript
// Logstash  예
input {
  file {
    path => "/path/to/log/file.log"
  }
}

filter {
  grok {
    match => { "message" => "%{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => "localhost:9200"
    index => "log-%{+yyyy.MM.dd}"
  }
}
```

```typescript
// 잘못된 사용 예
// 로그 파일 경로가 잘못된 경우
input {
  file {
    path => "/path/to/incorrect/log/file.log"
  }
}

// 올바른 사용 예
input {
  file {
    path => "/path/to/correct/log/file.log"
  }
}
```

### 비교 분석

| 구분 | ELK Stack | Loki | Fluentd |
|------|---------|------|---------|
| 로그 수집 | Logstash | Promtail | Fluentd |
| 로그 저장소 | Elasticsearch | Grafana Loki | 다양한 저장소 |
| 로그 분석 도구 | Kibana | Grafana | 다양한 도구 |

### 실전 팁
- 로그 수집 시, 로그 파일 경로와 이름을 정확하게 지정해야 합니다.
- 로그 분석 시, 적절한 쿼리와 필터를 사용하면 필요한 정보를 빠르게 찾을 수 있습니다.
- 성능을 위해, 로그 수집과 저장소를 분리하고, 적절한 자원 할당을 해야 합니다.

### 한 줄 정리
로그 수집과 분석은 시스템의 상태를 파악하고 문제를 진단하는 데 중요한 역할을 하는데 ELK Stack과 Loki는 이러한 기능을 제공합니다.