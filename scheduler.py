"""
스케줄링 모듈
- 지정된 시간에 자동 실행
"""

import schedule
import time
from datetime import datetime
from main import main
import pytz


def run_scheduled():
    """스케줄된 작업 실행"""
    try:
        print(f"\n⏰ 스케줄 실행 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        main()
    except Exception as e:
        print(f"❌ 스케줄 실행 오류: {e}")


def start_scheduler(run_time: str = "07:00", timezone: str = "Asia/Seoul"):
    """
    스케줄러 시작
    Args:
        run_time: 실행 시간 (HH:MM 형식)
        timezone: 시간대
    """
    # 매일 지정 시간에 실행
    schedule.every().day.at(run_time).do(run_scheduled)
    
    print(f"✅ 스케줄러 시작 - 매일 {run_time}에 실행")
    print("종료하려면 Ctrl+C를 누르세요.\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    except KeyboardInterrupt:
        print("\n⏹️ 스케줄러 종료")


if __name__ == "__main__":
    import config
    
    run_time = getattr(config, 'AUTO_RUN_TIME', '07:00')
    timezone = getattr(config, 'TIMEZONE', 'Asia/Seoul')
    
    start_scheduler(run_time, timezone)
