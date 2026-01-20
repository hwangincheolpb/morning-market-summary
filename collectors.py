"""
시황 데이터 수집 모듈
- 텔레그램 채널에서 마감시황 메시지 수집 (Telethon 사용)
- Alpha Vantage API로 뉴스 및 감성 분석 수집
- yfinance로 주요 지수 데이터 수집
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import re


class TelegramChannelCollector:
    """텔레그램 채널에서 마감시황 수집 (웹 스크래핑 방식)"""

    def __init__(self, channel_username: str):
        self.channel_username = channel_username
        self.base_url = f"https://t.me/s/{channel_username}"

    def get_latest_message(self) -> Optional[str]:
        """
        텔레그램 채널의 최신 메시지 가져오기
        참고: 텔레그램 공개 채널은 웹에서 직접 접근 가능
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(self.base_url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 텔레그램 웹 버전의 메시지 구조 파싱
            messages = soup.find_all('div', class_='tgme_widget_message_text')

            if messages:
                # 최신 메시지 추출 (가장 마지막)
                latest_text = messages[-1].get_text(separator='\n', strip=True)
                return latest_text

            return None

        except Exception as e:
            print(f"⚠️ 텔레그램 채널 수집 오류: {e}")
            return None

    def get_today_messages(self) -> List[str]:
        """오늘 날짜의 모든 메시지 가져오기"""
        try:
            # 오늘 날짜로 필터링된 메시지들
            today = datetime.now().strftime("%Y년 %m월 %d일")
            messages = []

            # 텔레그램 채널은 최신 메시지를 우선 가져오고 날짜로 필터링
            latest = self.get_latest_message()
            if latest and today in latest:
                messages.append(latest)

            return messages

        except Exception as e:
            print(f"⚠️ 오늘 메시지 수집 오류: {e}")
            return []


class AlphaVantageCollector:
    """Alpha Vantage API로 뉴스 및 감성 분석 수집"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_market_news(self, topics: str = "financial_markets", limit: int = 10) -> Optional[str]:
        """
        Alpha Vantage News & Sentiment API로 시장 뉴스 가져오기
        무료 티어: 25 requests/day, 5 requests/minute
        """
        try:
            params = {
                'function': 'NEWS_SENTIMENT',
                'topics': topics,
                'limit': limit,
                'apikey': self.api_key
            }

            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if 'feed' not in data:
                print(f"⚠️ Alpha Vantage API 응답 오류: {data.get('Note', data)}")
                return None

            # 뉴스 항목 포맷팅
            news_summary = []
            for item in data['feed'][:limit]:
                title = item.get('title', 'No title')
                summary = item.get('summary', '')
                sentiment_score = item.get('overall_sentiment_score', 0)
                sentiment_label = item.get('overall_sentiment_label', 'Neutral')

                news_summary.append(f"[{sentiment_label}] {title}\n{summary[:200]}...")

            return "\n\n".join(news_summary)

        except Exception as e:
            print(f"⚠️ Alpha Vantage 수집 오류: {e}")
            return None


class YFinanceCollector:
    """yfinance로 주요 지수 데이터 수집"""

    def __init__(self):
        try:
            import yfinance as yf
            self.yf = yf
        except ImportError:
            print("⚠️ yfinance 패키지가 설치되지 않았습니다. pip install yfinance로 설치하세요.")
            self.yf = None

    def get_market_indices(self) -> Optional[str]:
        """주요 지수 데이터 가져오기"""
        if not self.yf:
            return None

        try:
            # 주요 지수 티커
            indices = {
                'Dow Jones': '^DJI',
                'NASDAQ': '^IXIC',
                'S&P 500': '^GSPC',
                'VIX': '^VIX',
                'Dollar Index': 'DX-Y.NYB',
                'WTI Crude Oil': 'CL=F',
                '10-Year Treasury': '^TNX'
            }

            results = []
            for name, ticker in indices.items():
                try:
                    stock = self.yf.Ticker(ticker)
                    info = stock.history(period='2d')

                    if len(info) >= 2:
                        latest_close = info['Close'].iloc[-1]
                        prev_close = info['Close'].iloc[-2]
                        change_pct = ((latest_close - prev_close) / prev_close) * 100

                        results.append(f"{name}: {latest_close:.2f} ({change_pct:+.2f}%)")
                except Exception as e:
                    print(f"⚠️ {name} 데이터 수집 실패: {e}")
                    continue

            return "\n".join(results) if results else None

        except Exception as e:
            print(f"⚠️ yFinance 수집 오류: {e}")
            return None


def collect_all_sources(config) -> str:
    """
    모든 소스에서 시황 데이터 수집하여 통합
    """
    all_texts = []

    # 1. 텔레그램 채널 수집
    if hasattr(config, 'TELEGRAM_CHANNEL_USERNAME') and config.TELEGRAM_CHANNEL_USERNAME:
        telegram_collector = TelegramChannelCollector(config.TELEGRAM_CHANNEL_USERNAME)
        telegram_msg = telegram_collector.get_latest_message()
        if telegram_msg:
            all_texts.append(f"[텔레그램 채널 시황]\n{telegram_msg}")
            print("✅ 텔레그램 채널 데이터 수집 완료")
        else:
            print("⚠️ 텔레그램 채널 데이터 수집 실패")

    # 2. Alpha Vantage 뉴스 수집
    if hasattr(config, 'ALPHA_VANTAGE_API_KEY') and config.ALPHA_VANTAGE_API_KEY:
        av_collector = AlphaVantageCollector(config.ALPHA_VANTAGE_API_KEY)
        news_data = av_collector.get_market_news(topics='financial_markets', limit=5)
        if news_data:
            all_texts.append(f"[Alpha Vantage 시장 뉴스]\n{news_data}")
            print("✅ Alpha Vantage 뉴스 수집 완료")
        else:
            print("⚠️ Alpha Vantage 뉴스 수집 실패")

    # 3. yFinance 지수 데이터 수집
    yf_collector = YFinanceCollector()
    indices_data = yf_collector.get_market_indices()
    if indices_data:
        all_texts.append(f"[주요 지수 데이터]\n{indices_data}")
        print("✅ 주요 지수 데이터 수집 완료")
    else:
        print("⚠️ 주요 지수 데이터 수집 실패")

    if not all_texts:
        raise Exception("수집된 데이터가 없습니다. 최소 1개 이상의 데이터 소스가 필요합니다.")

    return "\n\n" + "="*60 + "\n\n".join(all_texts)
