# 아침 시황 요약 자동화 - 구현 가이드

## 📋 프로젝트 개요

텔레그램 채널과 웹사이트에서 마감시황을 자동으로 수집하여, Gemini API로 요약하고 텔레그램으로 발송하는 시스템입니다.

## 🔧 설치 방법

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 설정 파일 생성

```bash
# Windows
copy config.py.example config.py

# Linux/Mac
cp config.py.example config.py
```

### 3. config.py 설정

`config.py` 파일을 열어서 다음 항목을 채워주세요:

#### 필수 설정

1. **Gemini API 키**
   ```python
   GEMINI_API_KEY = "여기에_발급받은_Gemini_API_키_입력"
   ```
   - 발급 방법: https://makersuite.google.com/app/apikey

2. **텔레그램 봇 토큰** (발송용)
   ```python
   TELEGRAM_BOT_TOKEN = "여기에_봇_토큰_입력"
   TELEGRAM_SEND_TO_CHAT_ID = "여기에_내_채팅_ID_입력"
   ```
   - 봇 만들기: 텔레그램에서 @BotFather에게 `/newbot` 명령
   - 채팅 ID 확인: @userinfobot에게 메시지 보내기

#### 선택 설정

3. **자동 실행 시간**
   ```python
   AUTO_RUN_TIME = "07:00"  # 아침 7시
   ```

4. **양식 선택**
   ```python
   USE_DETAILED_FORMAT = False  # False: 간결 버전, True: 상세 버전
   ```

## 🚀 사용 방법

### 수동 실행

```bash
python main.py
```

### 자동 실행 (스케줄러)

```bash
python scheduler.py
```

스케줄러는 매일 지정된 시간에 자동으로 실행됩니다.

## 📁 파일 구조

```
아침_시황_요약_자동화/
├── main.py              # 메인 스크립트
├── collectors.py        # 데이터 수집 모듈
├── gemini_summarizer.py # Gemini 요약 모듈
├── sender.py           # 발송 모듈
├── scheduler.py        # 스케줄링 모듈
├── config.py           # 설정 파일 (직접 생성)
├── config.py.example   # 설정 예시
├── requirements.txt    # 필수 패키지
└── output/             # 출력 파일 저장 폴더
```

## 🔍 데이터 소스

1. **텔레그램 채널**: https://t.me/shmstory
   - 시황맨의 주식이야기 채널
   - 마감시황 텍스트 메시지 수집

2. **웹사이트**: https://www.briefing.com/stock-market-update
   - 마감 후 30분 정도 안에 마감시황 업데이트
   - 웹 스크래핑으로 수집

## 📝 출력 양식

간결 버전 (기본):
```
신한투자증권 서울금융센터 황인철PB입니다.

🇺🇸 [날짜] 미국 증시: [핵심 키워드]

✅ 핵심 요약
 * [핵심 요약 1]
 * [핵심 요약 2]
 * [핵심 요약 3]

📊 주요 지수
...

📉 매크로 지표
...

감사합니다.
```

## ⚠️ 주의사항

1. **텔레그램 채널 접근**: 
   - 텔레그램 웹 버전에서 공개 채널은 접근 가능하지만, 구조가 변경될 수 있습니다.
   - 필요시 텔레그램 API를 사용하는 방법으로 변경해야 할 수 있습니다.

2. **웹사이트 스크래핑**:
   - Briefing.com의 실제 HTML 구조에 맞게 파싱 로직을 조정해야 할 수 있습니다.
   - 처음 실행 시 실제 HTML 구조를 확인하여 수정하세요.

3. **API 제한**:
   - Gemini API: 무료 버전은 사용량 제한이 있을 수 있습니다.
   - 텔레그램 봇: 분당 메시지 수 제한이 있습니다.

## 🐛 문제 해결

### 텔레그램 채널 수집 실패
- 채널이 공개 채널인지 확인
- 텔레그램 웹 버전에서 접근 가능한지 확인
- 필요시 텔레그램 Bot API 사용 고려

### 웹사이트 수집 실패
- 브라우저에서 해당 페이지 접근 가능한지 확인
- HTML 구조가 변경되었을 수 있으므로 실제 구조 확인 후 수정

### Gemini API 오류
- API 키가 유효한지 확인
- 사용량 제한 확인
- 프롬프트가 너무 길지 않은지 확인

## 📞 지원

문제가 발생하면 로그를 확인하고, 각 모듈의 오류 메시지를 참고하세요.
