import os
import requests
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord_webhook(content):
    """브리핑 내용을 디스코드 웹훅으로 전송"""
    if not DISCORD_WEBHOOK_URL:
        print("[오류] DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return False

    # 디스코드 메시지 길이 제한 (2000자) 대응
    if len(content) > 2000:
        chunks = [content[i:i+1990] for i in range(0, len(content), 1990)]
        for chunk in chunks:
            data = {"content": chunk}
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)
            if response.status_code not in (200, 204):
                print(f"[오류] 웹훅 전송 실패: {response.status_code} - {response.text}")
                return False
        print("[성공] 분할된 브리핑이 웹훅을 통해 전송되었습니다.")
        return True
    else:
        data = {"content": content}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        
        if response.status_code in (200, 204):
            print("[성공] 브리핑이 웹훅을 통해 전송되었습니다.")
            return True
        else:
            print(f"[오류] 웹훅 전송 실패: {response.status_code} - {response.text}")
            return False
