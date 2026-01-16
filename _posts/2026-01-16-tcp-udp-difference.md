---
title: "[CS 지식] TCP와 UDP의 차이"
date: 2026-01-16 10:00:00 +0900
categories: [개발뉴스]
tags: [CS, 중급, 네트워크]
---

## TCP vs UDP, 뭐가 다를까?

택배와 편지로 비유해볼게요.

**TCP는 등기 택배** 📦
- 받는 사람이 확실히 받았는지 확인
- 순서대로 도착 보장
- 분실되면 다시 보냄

**UDP는 전단지** 📄
- 그냥 뿌리고 끝
- 받든 말든 신경 안 씀
- 대신 엄청 빠름

---

## 핵심 차이점

| 구분 | TCP | UDP |
|------|-----|-----|
| 연결 | 연결 필요 (3-way handshake) | 연결 없음 |
| 신뢰성 | 데이터 도착 보장 | 보장 안 함 |
| 순서 | 순서 보장 | 순서 보장 안 함 |
| 속도 | 느림 | 빠름 |
| 사용처 | 웹, 이메일, 파일 전송 | 스트리밍, 게임, DNS |

---

## 코드로 보는 차이

```python
# TCP 소켓
import socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('server.com', 80))

# UDP 소켓
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.sendto(data, ('server.com', 53))
```

---

## 면접 단골 질문

**Q: TCP 3-way handshake란?**

A: 연결 수립 과정입니다.
1. Client → Server: SYN (연결 요청)
2. Server → Client: SYN + ACK (요청 수락)
3. Client → Server: ACK (확인)

**Q: UDP를 쓰는 이유는?**

A: 속도가 중요하고 일부 데이터 손실이 괜찮은 경우 (실시간 스트리밍, 게임)

---

## 한 줄 요약

> **TCP는 신뢰성**, **UDP는 속도**. 용도에 맞게 선택하자!
