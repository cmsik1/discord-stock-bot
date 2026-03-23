import os
from google import genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini AI 설정
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 관심 종목
interest_stocks = "삼성전자, SK하이닉스, 현대차, 기아, 두산로보틱스"

def generate_briefing(market_data, news_data):
    """수집 데이터를 Gemini에게 보내 마크다운 브리핑을 생성"""
    prompt = f"""당신은 전문 주식 애널리스트입니다.
아래 데이터를 분석하여 **디스코드 메시지용 마크다운 브리핑**을 작성해 주세요.

## 제공 데이터

### 미국 주요 지수 (최신 마감)
{market_data}

### 네이버 금융 주요 뉴스
{news_data}

### 관심 종목
{interest_stocks}

## 작성 요청 사항
다음 세 가지 섹션을 포함해 주세요:
1. **시황 요약** - 미국 시장 동향과 뉴스를 종합한 간결한 시황 요약
2. **섹터 분석** - 관심 종목이 속한 섹터(반도체, 자동차, 로봇)의 전망
3. **오늘의 매매 전략** - 관심 종목 기반 구체적 매매 전략 제안

디스코드에 보내는 메시지이므로 2000자 이내로 작성해 주세요.
마크다운 형식으로 작성하되, 이모지를 적절히 활용해 가독성을 높여 주세요.
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
