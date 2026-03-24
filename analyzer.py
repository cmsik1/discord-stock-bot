import os
from google import genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini AI 설정
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_briefing(market_data, news_data, interest_stocks, today_date):
    """수집 데이터를 Gemini에게 보내 마크다운 브리핑을 생성"""
    prompt = f"""당신은 여의도의 복잡한 시황과 종목 분석을 주린이(초보 투자자)의 눈높이에 맞춰 아주 쉽고 명쾌하게 풀어주는 '1타 주식 멘토'입니다.

[오늘의 기초 데이터]

미국 주요 지수 마감: {market_data}

밤사이 핵심 뉴스: {news_data}

타겟 모니터링 종목: {interest_stocks}

[분석 및 출력 가이드라인 - 엄수]

인사말 금지: 바로 본론으로 시작하세요.

극단적 쉬운 용어 사용 (가장 중요): '디스인플레이션', '리스크 온', '디커플링', 'CAPEX', '숏커버링', '롱숏' 같은 어려운 증권사 전문 용어를 절대 사용하지 마세요. "물가 하락", "투자 심리 회복", "따로 노는 흐름", "기업 투자금", "오를 것으로 기대하고 사는 현상" 등 중학생도 이해할 수 있는 아주 쉬운 일상어로 풀어서 쓰세요.

탑다운 분석 (Macro -> Micro): [반도체, 방산, 로봇, 바이오] 4가지 섹터의 오늘 장 전체 분위기를 먼저 짚어주고, 타겟 모니터링 종목들에 대해서만 구체적인 가격 위치나 호재/악재를 분석하세요.

명확하고 짧은 문장: 한 문장이 너무 길어지지 않게 짧게 끊어서 가독성을 높이세요. 실전 트레이딩에 적용 가능한 액션 포인트는 두리뭉실하게 쓰지 말고 명확히 제시하세요.

[출력 마크다운 양식]

📅 {today_date} 모닝 브리핑
📊 간밤의 미국 증시
한줄 요약: (미 증시 핵심 흐름을 쉬운 말로 1줄 요약)

시장 분위기: (수집된 지수/뉴스 기반으로 2~3줄 요약)

🌊 4대 섹터 큰 흐름
💾 반도체: (쉬운 말로 1~2줄)

🛡️ 방산: (쉬운 말로 1~2줄)

🤖 로봇: (쉬운 말로 1~2줄)

🧬 바이오: (쉬운 말로 1~2줄)

🎯 내 관심 종목 현미경 분석
[종목명 1 & 2]: (어려운 용어 없이 상세 분석 및 대응 방법)

[종목명 3 & 4]: (어려운 용어 없이 상세 분석 및 대응 방법)
... (타겟 종목 위주로 묶어서 작성)

💡 오늘의 실전 매매 전략
(가장 중요한 첫 번째 전략/대응을 아주 쉽게 설명)

(두 번째 전략/대응)"""

    response = gemini_client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
    )
    return response.text
