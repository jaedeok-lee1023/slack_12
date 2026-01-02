import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-01-01",  # 신정
    "2026-02-16",  # 설 연휴
    "2026-02-17",  # 설날
    "2026-02-18",  # 설 연휴
    "2026-03-02",  # 대체공휴일
    "2026-05-05",  # 어린이날
    "2026-05-25",  # 대체공휴일
    "2026-06-03",  # 지방선거
    "2026-08-17",  # 대체공휴일
    "2026-09-24",  # 추석 연휴
    "2026-09-25",  # 추석
    "2026-10-05",  # 대체공휴일
    "2026-10-09",  # 한글날
    "2026-12-25",  # 크리스마스
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f"*[공지｜신규 입사자 Welcome Kit 수령 안 ]*\n\n\n"

        notice_msg = (
            f"1. *중요도* : 하\n"
            f"2. *대상* : 평택 클러스터 신규 입사\n"
            f"3. *주요 내용*\n\n"
            f"\n"
            f"*신규 입사자* Welcome Kit 불출 안내 드립니다.\n\n"
            f"\n"
            f"*• 대상* : *<https://docs.google.com/spreadsheets/d/1TCD-vMZekrLQsihs0kKJEFm2wCsWmtCjJquPCWRN9LQ/edit?gid=0#gid=0|대상자 명단>*\n"
            f"*• 장소* : *2층 통합사무실 인사총무_인사 (주말,공휴일 제외 / 10시 19시)*\n"
            f"*:slack: 문의사항 : 인사총무 인사팀 담당자*\n\n"
            f"\n"
            f"감사합니다. 😊\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
