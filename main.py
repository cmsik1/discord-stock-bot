import sys

# Windows 콘솔 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from scraper import get_us_market_data, get_naver_news
from analyzer import generate_briefing
from notifier import send_to_discord_webhook

def main():
    print("[1/3] 데이터 수집 중...")
    market_data = get_us_market_data()
    news_data = get_naver_news()

    print("[2/3] Gemini 브리핑 생성 중...")
    try:
        briefing = generate_briefing(market_data, news_data)
    except Exception as e:
        print(f"[오류] 브리핑 생성 실패: {e}")
        return

    print("[3/3] 디스코드 웹훅 전송 중...")
    success = send_to_discord_webhook(briefing)
    
    if success:
        print("모든 작업이 완료되었습니다.")
    else:
        print("작업 중 일부 오류가 발생했습니다.")

if __name__ == "__main__":
    main()
