import os
import requests
import bs4 as bs
import telebot
from random import choice

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
    with requests.session() as c:
        #head = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #        #"cookie": "wordpress_test_cookie=WP Cookie check",
        #        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Mobile Safari/537.36"}
        login_data = {"log": login,
                      "pwd": password,
                      'wp-submit': 'Log In',
                      'redirect_to': "https://w41k3r.com/wp-admin/",
                      'testcookie': '1',
                      "rememberme": "forever"}
        lpage = c.get(login_link)
        #print(lpage.text)
        log = c.post(login_link, data=login_data)
        #print(c.headers)
        #print(log.cookies)
        #head = random_headers()
        #page_login = c.post(login_link, data=login_data, headers=head)

        p = c.get(p_link, cookies=log.cookies) #, headers=head)
        temp = bs.BeautifulSoup(p.content, features="html.parser")
        #send_file(str(temp.find("main").encode("utf-8")))

        send_file(str(lpage.text.encode("utf-8")))

        #print(temp)
        #print(temp.find("main"))

def send_message(message):
    msg = bot.send_message(channel, message, parse_mode='Markdown', disable_web_page_preview=True)

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    parse_rss("https://w41k3r.com/i-know-why-they-are-riding-horses/")
