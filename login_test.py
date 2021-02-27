import os
import requests
import bs4 as bs
import telebot
import feedparser
from time import sleep
import hashlib as h
from random import choice

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

token = os.environ['TELEGRAM_TOKEN']
channel = os.environ['CHANNEL_ID']
login = os.environ['WALKER_LOGIN']
password = os.environ['WALKER_PASSWORD']

main_link = "https://w41k3r.com/"
rss_link = "https://w41k3r.com/feed"
comments_link = "https://w41k3r.com/comments/feed/"
login_link = "https://w41k3r.com/wp-login.php"
alan_link = "https://w41k3r.com/walkers/?w_id=0"

def send_file(code):
    text_file = open("parse.txt", "w")
    text_file.write(code)
    text_file.close()
    text_file = open("parse.txt", "r")
    msg = bot.send_document(channel, text_file)
    text_file.close()

def parse_rss(p_link):
            c = requests.session()
            login_data = {"log": login,
                          "pwd": password,
                          "rememberme": "forever",
                          "redirect_to": p_link,
                          "redirect_to_automatic": "1"}

            head = random_headers()
            page_login = c.post(login_link, data=login_data, headers=head)
            p = c.get(p_link, headers=head)
            temp = bs.BeautifulSoup(p.content, features="html.parser")
            send_file(str(temp.find("main").encode("utf-8")))

            #print(temp)
            #print(temp.find("main"))

def send_message(message):
    msg = bot.send_message(channel, message, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    parse_rss("https://w41k3r.com/i-know-why-they-are-riding-horses/")
