import os
import sys
import datetime

# Windows 콘솔 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import discord
from discord.ext import commands, tasks
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pytz
import google.generativeai as genai

# .env 파일에서 환경 변수 로드
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

# Gemini AI 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# 관심 종목
interest_stocks = "삼성전자, SK하이닉스, 현대차, 기아, 두산로보틱스"

# 한국 시간대
KST = pytz.timezone("Asia/Seoul")

# 평일 아침 8시 (KST) -> UTC 변환: 8시 KST = 23시 전날 UTC
# discord.ext.tasks는 UTC 기준이므로 time을 UTC로 지정
briefing_time = datetime.time(hour=23, minute=0, tzinfo=datetime.timezone.utc)

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ──────────────────────────────────────────────
# 데이터 수집 함수
# ──────────────────────────────────────────────

def get_us_market_data():
    """다우, 나스닥, S&P 500의 최신 마감 지수를 문자열로 반환"""
    indices = {
        "다우존스": "^DJI",
        "나스닥": "^IXIC",
        "S&P 500": "^GSPC",
    }

    results = []
    for name, ticker in indices.items():
        data = yf.Ticker(ticker)
        hist = data.history(period="1d")
        if not hist.empty:
            close = hist["Close"].iloc[-1]
            results.append(f"{name}: {close:,.2f}")
        else:
            results.append(f"{name}: 데이터 없음")

    return "\n".join(results)


def get_naver_news():
    """네이버 금융 메인 뉴스 헤드라인 5개를 문자열로 반환"""
    url = "https://finance.naver.com/news/mainnews.naver"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.encoding = "euc-kr"
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    news_items = soup.select("dd.articleSubject a")
    for item in news_items[:5]:
        title = item.get_text(strip=True)
        headlines.append(title)

    if not headlines:
        return "뉴스를 가져올 수 없습니다."

    result = []
    for i, title in enumerate(headlines, 1):
        result.append(f"{i}. {title}")

    return "\n".join(result)


# ──────────────────────────────────────────────
# Gemini AI 브리핑 생성
# ──────────────────────────────────────────────

async def generate_briefing():
    """수집 데이터를 Gemini에게 보내 마크다운 브리핑을 생성"""
    market_data = get_us_market_data()
    news_data = get_naver_news()

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

    response = model.generate_content(prompt)
    return response.text


# ──────────────────────────────────────────────
# 디스코드 채널 전송
# ──────────────────────────────────────────────

async def send_briefing_to_channel():
    """브리핑을 생성하여 지정 채널에 전송"""
    if not DISCORD_CHANNEL_ID:
        print("[오류] DISCORD_CHANNEL_ID가 설정되지 않았습니다.")
        return

    channel = bot.get_channel(int(DISCORD_CHANNEL_ID))
    if channel is None:
        print(f"[오류] 채널 ID {DISCORD_CHANNEL_ID}를 찾을 수 없습니다.")
        return

    try:
        briefing = await generate_briefing()
        # 디스코드 메시지 길이 제한 (2000자) 대응
        if len(briefing) > 2000:
            # 여러 메시지로 분할 전송
            chunks = [briefing[i:i+1990] for i in range(0, len(briefing), 1990)]
            for chunk in chunks:
                await channel.send(chunk)
        else:
            await channel.send(briefing)
        print(f"[성공] 브리핑이 채널에 전송되었습니다. ({datetime.datetime.now(KST).strftime('%Y-%m-%d %H:%M')})")
    except Exception as e:
        print(f"[오류] 브리핑 전송 실패: {e}")


# ──────────────────────────────────────────────
# 스케줄러: 평일 아침 8시 (KST) 자동 실행
# ──────────────────────────────────────────────

@tasks.loop(time=briefing_time)
async def morning_briefing():
    """평일(월~금) 아침 8시(KST)에 자동 브리핑 전송"""
    now = datetime.datetime.now(KST)
    # 평일(월=0 ~ 금=4)에만 실행
    if now.weekday() < 5:
        print(f"[스케줄러] 평일 아침 브리핑 시작 ({now.strftime('%Y-%m-%d %H:%M')})")
        await send_briefing_to_channel()
    else:
        print(f"[스케줄러] 주말이므로 브리핑을 건너뜁니다. ({now.strftime('%Y-%m-%d %A')})")


@morning_briefing.before_loop
async def before_morning_briefing():
    """봇이 완전히 준비될 때까지 대기"""
    await bot.wait_until_ready()


# ──────────────────────────────────────────────
# 봇 이벤트 & 명령어
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"[봇 시작] {bot.user.name} 로그인 완료!")
    print(f"[설정] 브리핑 채널 ID: {DISCORD_CHANNEL_ID}")
    print(f"[설정] 스케줄: 평일 08:00 KST")
    if not morning_briefing.is_running():
        morning_briefing.start()
        print("[스케줄러] 아침 브리핑 스케줄러가 시작되었습니다.")


@bot.command(name="브리핑")
async def manual_briefing(ctx):
    """수동으로 브리핑을 요청하는 명령어"""
    await ctx.send("브리핑을 생성 중입니다... 잠시만 기다려 주세요.")
    try:
        briefing = await generate_briefing()
        if len(briefing) > 2000:
            chunks = [briefing[i:i+1990] for i in range(0, len(briefing), 1990)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(briefing)
    except Exception as e:
        await ctx.send(f"브리핑 생성 중 오류가 발생했습니다: {e}")


# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if DISCORD_TOKEN:
        bot.run(DISCORD_TOKEN)
    else:
        print("[오류] DISCORD_TOKEN이 설정되지 않았습니다. .env 파일을 확인해 주세요.")
