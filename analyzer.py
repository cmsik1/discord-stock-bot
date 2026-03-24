import os
from google import genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini AI 설정
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_briefing(market_data, news_data, interest_stocks):
    """수집 데이터를 Gemini에게 보내 마크다운 브리핑을 생성"""
    prompt = f"""당신은 월스트리트의 거시경제 데이터와 여의도의 자금 흐름을 꿰뚫어 보는 20년 차 탑 티어 수석 전략가입니다.

[오늘의 기초 데이터]

미국 주요 지수 마감: {market_data}

밤사이 핵심 뉴스: {news_data}

타겟 모니터링 종목: {interest_stocks}

[분석 및 출력 가이드라인 - 엄수]

인사말 금지: 바로 본론으로 시작하세요.

탑다운 분석 (Macro -> Micro): [반도체, 방산, 로봇, 바이오] 4가지 메가 트렌드 섹터의 오늘 장 전체 흐름을 먼저 짚어주세요. 그 후, 타겟 모니터링 종목들에 대해서만 모멘텀, 수급, 가격 위치 등을 훨씬 깊이 있게 개별 분석하세요.

명확성: 애매모호한 전망은 배제하고, 실전 트레이딩에 적용 가능한 명확한 액션 포인트를 도출하세요. 전문 용어는 문맥에 맞게 자연스럽게 사용하되, 별도의 용어 설명은 덧붙이지 마세요.

[출력 마크다운 양식]

📊 Wall Street Overnight
한줄 요약: (미 증시 핵심 흐름 1줄)

시장 동향: (수집된 지수/뉴스 기반으로 2~3줄 요약)

🌊 4대 섹터 메가 트렌드 (Macro)
💾 반도체: (큰 흐름 1~2줄)

🛡️ 방산: (큰 흐름 1~2줄)

🤖 로봇: (큰 흐름 1~2줄)

🧬 바이오: (큰 흐름 1~2줄)

🎯 관심 종목 딥다이브 (Micro)
(타겟 모니터링 종목들의 구체적 파급 효과, 가격 위치, 호재/악재 분석)

[종목명 1 & 2]: (상세 분석 및 매매 뷰)

[종목명 3 & 4]: (상세 분석 및 매매 뷰)
... (타겟 종목 위주로 묶어서 작성)

💡 오늘의 매매 액션 플랜
(가장 중요한 첫 번째 전략/대응)

(두 번째 전략/대응)"""

    response = gemini_client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
    )
    return response.text
