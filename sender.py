"""
발송 모듈
- 텔레그램 봇으로 메시지 발송 (python-telegram-bot v20+ 사용)
"""

from telegram import Bot
import asyncio
from typing import Optional


async def send_telegram_message(bot: Bot, chat_id: int, message: str) -> bool:
    """
    텔레그램 메시지 전송

    Args:
        bot: telegram.Bot 인스턴스
        chat_id: 발송할 채팅 ID (숫자)
        message: 발송할 메시지

    Returns:
        bool: 성공 여부
    """
    try:
        # 텔레그램 메시지 최대 길이 4096자 제한
        if len(message) > 4096:
            print(f"📨 메시지 길이 초과: {len(message)}자, 분할 전송")
            for i in range(0, len(message), 4096):
                chunk = message[i:i+4096]
                await bot.send_message(chat_id=chat_id, text=chunk)
                print(f"  ✓ 분할 전송: {i} ~ {i+len(chunk)}")
                await asyncio.sleep(1)  # 연속 발송 시 딜레이
        else:
            await bot.send_message(chat_id=chat_id, text=message)

        print(f"✅ 텔레그램 전송 성공 (Chat ID: {chat_id})")
        return True
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패 (Chat ID: {chat_id}): {e}")
        return False


def send_summary(summary: str, config) -> bool:
    """
    요약 메시지를 텔레그램으로 발송

    Args:
        summary: 발송할 요약 메시지
        config: 설정 객체

    Returns:
        bool: 성공 여부
    """
    try:
        # 설정 검증
        if not hasattr(config, 'TELEGRAM_BOT_TOKEN') or not config.TELEGRAM_BOT_TOKEN:
            print("⚠️ TELEGRAM_BOT_TOKEN이 설정되지 않았습니다.")
            return False

        if not hasattr(config, 'TELEGRAM_SEND_TO_CHAT_ID') or not config.TELEGRAM_SEND_TO_CHAT_ID:
            print("⚠️ TELEGRAM_SEND_TO_CHAT_ID가 설정되지 않았습니다.")
            return False

        # Bot 인스턴스 생성
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)

        # 비동기 함수 실행
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            send_telegram_message(bot, config.TELEGRAM_SEND_TO_CHAT_ID, summary)
        )

    except Exception as e:
        print(f"❌ 발송 오류: {e}")
        import traceback
        traceback.print_exc()
        return False
