from crawler.constants import DISCORD_BOT_TOKEN, DISCORD_CHAT_LINK
import requests

def send_message(message):
    try:
        url = DISCORD_CHAT_LINK
        data = {'content': message}
        header = {'authorization': DISCORD_BOT_TOKEN}
        r = requests.post(url, data=data, headers=header)
        print(r.status_code)
    except Exception as ex:
        print(ex)