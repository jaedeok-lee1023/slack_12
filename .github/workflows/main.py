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
    "2025-01-01",  # 신정
    "2025-03-01",  # 삼일절
    "2025-05-05",  # 어린이날
    "2025-05-06",  # 대체공휴일
    "2025-06-06",  # 현충일
    "2025-08-15",  # 광복절
    "2025-10-03",  # 개천절
    "2025-10-06",  # 추석
    "2025-10-07",  # 추석연휴
    "2025-10-08",  # 대체공휴일
    "2025-10-09",  # 한글날
    "2025-12-25",  # 크리스마스
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
        header = f":loudspeaker: *『인사총무팀 공지』* <!channel>\n\n"

        notice_msg = (
            f"안녕하세요? 평택 클러스터 구성원 여러분!\n"
            f"\n"
            f" 효율적인 업무 인수인계와 원활한 퇴사 절차를 위해,\n"
            f" 기존의 퇴사 관련 규정을 다시 한번 확인하시어 준수해주시기를 바랍니다.\n"
            f" 이는 구성원 여러분의 권익 보호를 위한 중요한 사항이니 적극적인 협조 부탁드립니다.\n\n"
            f"\n"
            f":one: *사전합의 필수*\n"
            f">퇴사 의향이 있으신 경우, 반드시 부서 관리자와 사전 협의 후 관련 절차를 진행 및 안내 받으시길 바랍니다.\n\n"
            f":two: *퇴사일 사전 공유 기한*\n"
            f"> - *규칙* : 퇴사 예정일 30일 전\n"
            f"> - *최소* : 퇴사 예정일 15일 전\n\n"
            f":three: *무단 결근 및 결근 남용 금지*\n"
            f">사전 합의 없는 결근 후 퇴사는 삼가주시고, 출근이 어려울 경우 지체 없이 부서 관리자와 상의해 주시길 바랍니다.\n\n"
            f":four: *문의사항*\n"
            f"인사총무_담당자 : <@U05P7L2PDG9> <@U05NEF6RNDV>\n\n"
            f"\n"
            f" 감사합니다.\n"
            f"\n"
            f" * :point_right: <https://static.wixstatic.com/media/50072f_d531fd60687547569486ec7f2cf74a31~mv2.jpg|퇴사 프로세스 공지>*\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
