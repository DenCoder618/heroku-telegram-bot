import os
import requests
import bs4 as bs
import telebot
import feedparser
from time import sleep
import hashlib as h

token = os.environ['TELEGRAM_TOKEN']
channel = os.environ['CHANNEL_ID']
login = os.environ['WALKER_LOGIN']
password = os.environ['WALKER_PASSWORD']

main_link = "https://w41k3r.com/"
rss_link = "https://w41k3r.com/feed"
comments_link = "https://w41k3r.com/comments/feed/"
login_link = "https://w41k3r.com/wp-login.php"
alan_link = "https://w41k3r.com/walkers/?w_id=0"

def parse_rss(link):
    global old_hashes
    feed = feedparser.parse(link)
    hashes = []
    for entry in feed.entries:
        #print(str(entry.link))
        hash = h.md5(entry.link.encode('utf-8')).hexdigest()
        hashes.append(hash)
        if not hash in old_hashes:
            p_link = entry['links'][0]['href']
            c = requests.session()
            login_data = {"log": login, "pwd": password, "rememberme": "forever", "redirect_to": main_link, "redirect_to_automatic": "1"} page_login = c.post(login_link, data=login_data)
            p = c.get(link)
            s = bs.BeautifulSoup(p.content, features="html.parser").find("main")
            title = s.find("h1").text
            wid = s.find("span", {'class': 'wid'}).text
            t = s.find("article").text
            while "\n\n" in t: t = t.replace("\n\n", "\n")
            if t.startswith("\n"): t = t[1:]
            if t.endswith("\n"): t = t[:-1]
            mess = "Post by #" + wid + "\n" + title + "\n\n" + t + "\n\n" + p_link
            send_message(mess)
    old_hashes = hashes

def send_message(message):
    msg = bot.send_message(channel, message, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    old_hashes = [h.md5("lol".encode('utf-8')).hexdigest()]
    while True:
        parse_rss(rss_link)
        sleep(2)
