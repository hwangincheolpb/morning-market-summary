# 빠른 시작 가이드 ⚡

## 1단계: 필수 패키지 설치 (1분)

```bash
cd "c:\Claudecode\아침_시황_요약_자동화"
pip install -r requirements.txt
```

## 2단계: 설정 파일 생성 (3분)

### (1) 설정 파일 복사
```bash
copy config.py.example config.py
```

### (2) API 키 입력

`config.py` 파일을 열어서 다음 3가지를 입력하세요:

#### ① Gemini API 키
```python
GEMINI_API_KEY = "여기에_입력"
```
- 발급: https://makersuite.google.com/app/apikey

#### ② 텔레그램 봇 토큰
```python
TELEGRAM_BOT_TOKEN = "여기에_입력"
```
- 텔레그램에서 @BotFather 검색 → `/newbot` 입력

#### ③ 텔레그램 채팅 ID
```python
TELEGRAM_SEND_TO_CHAT_ID = 123456789  # 숫자만
```
- 텔레그램에서 @userinfobot 검색 → 메시지 보내기

## 3단계: 테스트 실행 (1분)

```bash
python test_collectors.py
```

성공하면:
```
✅ 텔레그램 채널: 성공
✅ yFinance 지수: 성공
```

## 4단계: 전체 실행 (1분)

```bash
python main.py
```

성공하면 텔레그램으로 시황 요약이 도착합니다!

## 5단계: 자동 실행 설정 (Windows)

### 방법 1: Python 스케줄러 (권장)

```bash
python scheduler.py
```

- 매일 오전 7시 자동 실행
- 시간 변경: config.py에서 `AUTO_RUN_TIME` 수정
- 종료: Ctrl+C

### 방법 2: Windows 작업 스케줄러

#### (1) 배치 파일 생성

`run_daily.bat` 파일을 만들고:

```batch
@echo off
cd /d "c:\Claudecode\아침_시황_요약_자동화"
python main.py
pause
```

#### (2) Windows 작업 스케줄러 등록

1. Windows 검색 → "작업 스케줄러"
2. "기본 작업 만들기" 클릭
3. 이름: "아침 시황 요약"
4. 트리거: "매일" → 오전 7시
5. 동작: "프로그램 시작" → `run_daily.bat` 선택
6. 완료!

## 문제 해결

### "GEMINI_API_KEY가 설정되지 않았습니다"
→ config.py 파일에 키 입력했는지 확인

### "텔레그램 전송 실패"
→ 봇에게 먼저 `/start` 메시지 보내기

### "수집된 데이터가 없습니다"
→ 인터넷 연결 확인

---

**완료! 이제 매일 자동으로 시황 요약을 받을 수 있습니다!** 🎉
