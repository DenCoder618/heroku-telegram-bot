import requests as r
import json as j
import os
import telebot
from time import sleep

token = os.environ['TELEGRAM_TOKEN']
channel = os.environ['CHANNEL_ID']
url = os.environ["VIDEO_URL"]
timeout = int(os.environ["TIMEOUT"])

yes = False
old = 0

def send_message(message):
    msg = bot.send_message(channel, message, parse_mode='Markdown', disable_web_page_preview=True)

#### MAIN ####

bot = telebot.TeleBot(token)
while True:
    parsed = int(j.loads(r.get(url).text)["items"][0]["statistics"]["viewCount"])
    if (parsed != old):
        if (parsed < 3000000000):
            d = 3000000000 - parsed
            text = "Left: `" + str(d) + "`\nNow: `" + str(parsed) + "`"
        else:
            if yes:
                text = "Now: `" + str(parsed) + "`"
            else:
                text = "🎉 YES! 3 billion is here! 🎉" + "\nNOW: " + str(parsed) + " !"
                yes = True
        send_message(text)
        old = parsed
    sleep(timeout)

#url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id=60ItHLz5WEA&key=AIzaSyDKkMbZiC1OMZ_rD6SxM4UpACW98ccAXC0"
