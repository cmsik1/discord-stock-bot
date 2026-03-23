# 📈 Discord Stock Briefing Bot

매일 아침(평일 08:00 KST) 미국 주요 주식 지수와 네이버 금융 핵심 뉴스를 크롤링하여 **Gemini AI**가 요약한 시황 브리핑을 디스코드(Discord) 채널로 자동 전송하는 봇입니다. 

## 🌟 주요 기능 (Features)
- **미국 주요 지수 스크래핑**: `yfinance`를 활용한 다우존스, 나스닥, S&P 500 최신 마감 지수 수집
- **한국 금융 뉴스 헤드라인**: `BeautifulSoup`을 통한 네이버 금융 메인 뉴스 상위 5개 수집
- **AI 시황 분석**: 수집된 데이터를 바탕으로 `Gemini 2.5 Flash` 모델이 시황 요약, 섹터 분석, 매매 전략을 포함한 리뷰 작성
- **완전 자동화 (Serverless)**: 별도의 24시간 서버 없이 **GitHub Actions**의 크론(cron) 스케줄러로 평일 지정된 시간에 스크립트 실행
- **디스코드 웹훅 연동**: 디스코드 채널에 깔끔한 마크다운 형식으로 분기(길이 초과 시 자동 분할) 전송

## 🛠️ 기술 스택 (Tech Stack)
- **언어**: Python 3.12
- **라이브러리**:
  - `yfinance` (해외 주가 데이터 수집)
  - `beautifulsoup4`, `requests` (웹 크롤링)
  - `google-genai` (Gemini API 텍스트 생성)
  - `python-dotenv` (로컬 환경 변수 관리)
- **배포 및 자동화**: GitHub Actions (CI/CD, Cron Scheduling)
- **알림 채널**: Discord Webhook

## ⚙️ 동작 원리 (Architecture)
코드 구조는 유지보수와 확장을 고려하여 3개의 주요 모듈로 분리되어 있습니다:
1. `scraper.py`: 데이터를 수집(Scraping)합니다. (미국 3대 지수, 네이버 뉴스 등)
2. `analyzer.py`: 수집된 데이터를 바탕으로 Gemini API(Prompting)를 통해 투자 브리핑 텍스트를 생성합니다.
3. `notifier.py`: 작성된 텍스트를 디스코드 길이 제한(2000자)에 맞춰 분할한 뒤, `requests` 패키지를 이용해 Discord Webhook으로 전송합니다.
4. `main.py`: 위의 3단계(수집 -> 분석 -> 전송)를 순차적으로 실행하는 메인 파이프라인 스크립트입니다.
5. `.github/workflows/briefing.yml`: GitHub Actions 환경에서 평일 오전 8시에 `main.py`를 실행하도록 자동화 스케줄을 담당합니다.

## 🚀 설정 및 실행 방법 (How to Run)
### 1. 로컬 환경 (수동 테스트)
```bash
# 패키지 설치
pip install -r requirements.txt

# .env 파일 세팅 (루트 폴더)
GEMINI_API_KEY=당신의_제미나이_API키
DISCORD_WEBHOOK_URL=당신의_디스코드_웹훅주소

# 스크립트 실행
python main.py
```

### 2. 클라우드 자동화 (GitHub Actions)
해당 저장소를 Fork하거나 업로드한 뒤, **Settings > Secrets and variables > Actions** 경로로 들어가 Repository secrets 2개를 추가합니다:
- `GEMINI_API_KEY`
- `DISCORD_WEBHOOK_URL`
설정이 끝나면 매일 한국 시간 평일 08:00에 디스코드로 브리핑이 날아옵니다. 수동으로 `Actions` 탭에서 workflow를 실행해 볼 수도 있습니다.
