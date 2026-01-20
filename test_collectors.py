"""
데이터 수집 모듈 테스트 스크립트
"""

from collectors import TelegramChannelCollector, YFinanceCollector, AlphaVantageCollector

print("=" * 60)
print("데이터 수집 모듈 테스트")
print("=" * 60)

# 1. 텔레그램 채널 테스트
print("\n[1] 텔레그램 채널 수집 테스트")
print("-" * 60)
telegram_collector = TelegramChannelCollector("shmstory")
telegram_msg = telegram_collector.get_latest_message()
if telegram_msg:
    print(f"✅ 성공! 메시지 길이: {len(telegram_msg)}자")
    print(f"미리보기:\n{telegram_msg[:300]}...")
else:
    print("❌ 실패")

# 2. yFinance 테스트
print("\n[2] yFinance 지수 데이터 수집 테스트")
print("-" * 60)
yf_collector = YFinanceCollector()
indices = yf_collector.get_market_indices()
if indices:
    print(f"✅ 성공!\n{indices}")
else:
    print("❌ 실패")

# 3. Alpha Vantage 테스트 (API 키가 있을 경우만)
print("\n[3] Alpha Vantage 뉴스 수집 테스트")
print("-" * 60)
print("⚠️ API 키가 필요합니다. config.py에 ALPHA_VANTAGE_API_KEY를 설정하세요.")
print("   발급: https://www.alphavantage.co/support/#api-key")

print("\n" + "=" * 60)
print("테스트 완료")
print("=" * 60)
