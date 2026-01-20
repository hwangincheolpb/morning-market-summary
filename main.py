"""
아침 시황 요약 자동화 - 메인 스크립트
"""

import sys
import os
from datetime import datetime

# config 모듈 import
try:
    import config
except ImportError:
    print("❌ config.py 파일이 없습니다. config.py.example을 복사하여 config.py를 만들고 설정을 입력하세요.")
    sys.exit(1)

from collectors import collect_all_sources
from gemini_summarizer import GeminiSummarizer
from sender import send_summary


def main():
    """메인 워크플로우"""
    print("=" * 50)
    print(f"아침 시황 요약 자동화 시작 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # 1. 시황 데이터 수집
        print("\n[1단계] 시황 데이터 수집 중...")
        market_data = collect_all_sources(config)
        
        if not market_data:
            raise Exception("수집된 데이터가 없습니다.")
        
        print(f"✅ 데이터 수집 완료 ({len(market_data)} 글자)")
        
        # 2. Gemini로 요약 생성
        print("\n[2단계] Gemini API로 요약 생성 중...")
        if not hasattr(config, 'GEMINI_API_KEY') or not config.GEMINI_API_KEY:
            raise Exception("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        use_detailed = getattr(config, 'USE_DETAILED_FORMAT', False)
        summarizer = GeminiSummarizer(
            api_key=config.GEMINI_API_KEY,
            use_detailed=use_detailed
        )
        
        summary = summarizer.summarize(market_data)
        
        if not summary:
            raise Exception("요약 생성 실패")
        
        print("✅ 요약 생성 완료")
        print("\n" + "=" * 50)
        print("생성된 요약:")
        print("=" * 50)
        print(summary)
        print("=" * 50)
        
        # 3. 발송
        print("\n[3단계] 메시지 발송 중...")
        send_success = send_summary(summary, config)
        
        if send_success:
            print("✅ 발송 완료")
        else:
            print("⚠️ 발송 실패 또는 발송 설정이 없습니다.")
            print("발송하지 않고 요약만 출력합니다.")
        
        # 4. 파일 저장 (선택)
        save_to_file(summary)
        
        print("\n✅ 전체 프로세스 완료!")
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


def save_to_file(summary: str):
    """요약을 파일로 저장"""
    try:
        os.makedirs("output", exist_ok=True)
        filename = f"output/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"💾 파일 저장: {filename}")
    except Exception as e:
        print(f"⚠️ 파일 저장 실패: {e}")


if __name__ == "__main__":
    main()
