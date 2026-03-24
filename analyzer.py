import os
from google import genai
from dotenv import load_dotenv
from prompt_template import PROMPT_V4_5

# .env 파일에서 환경 변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini AI 설정
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_briefing(market_data, news_data, interest_stocks, today_date):
    """수집 데이터를 Gemini에게 보내 마크다운 브리핑을 생성"""
    
    # 별도 파일(prompt_template.py)에서 가져온 템플릿에 데이터 채우기
    prompt = PROMPT_V4_5.format(
        market_data=market_data,
        news_data=news_data,
        interest_stocks=interest_stocks,
        today_date=today_date
    )

    response = gemini_client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
    )
    return response.text
