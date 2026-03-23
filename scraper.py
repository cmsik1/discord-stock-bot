import yfinance as yf
import requests
from bs4 import BeautifulSoup

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
