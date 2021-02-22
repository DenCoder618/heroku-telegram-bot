#from typing import Any
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

posts = []
comments = []

class Post:
    def __init__(self, data):
        # if data != '':
        self.title = ''
        self.author = data.find('span').text
        self.url = data.get('href')
        self.date = data.find('p').text.split(' – ')[1][10:]
        self.text = data.find('h2').text.split(' - ')[1]
class Comment:
    def __init__(self, data, author):
        # if data != '':
        self.author = author
        self.url = data.get('href')
        self.text = data.find('h2').text[1:-1]
        self.date = data.find_all('p')[1].text[14:]

def parse_post(link):
    c = requests.session()
    login_data = {"log": login,
                  "pwd": password,
                  "rememberme": "forever",
                  "redirect_to": main_link,
                  "redirect_to_automatic": "1"}
    page_login = c.post(login_link, data=login_data)
    p = c.get(link)
    s = bs.BeautifulSoup(p.text, features="html.parser").find("main")

    title = s.find("h1").text
    wid = s.find("span", {'class': 'wid'}).text
    t = s.find("article").text
    while "\n\n" in t: t = t.replace("\n\n", "\n")
    if t.startswith("\n"): t = t[1:]
    if t.endswith("\n"): t = t[:-1]
    return wid, title, t

def potato_parser():
    c = requests.session()
    login_data = {"log": login,
                  "pwd": password,
                  "rememberme": "forever",
                  "redirect_to": main_link,
                  "redirect_to_automatic": "1"}
    page_login = c.post(login_link, data=login_data)
    print(page_login)

    page = c.get(alan_link)
    soup = bs.BeautifulSoup(page.text, features="html.parser")
    main = soup.find('main', {'class': 'items'})

def format_out():
    output = "POSTS:\n"
    for p in posts:
        output += "[" + p.date + "]\n(" + p.author + ') - ' + p.text + "\n\n"
    output += "COMMENTS:\n"
    for c in comments:
        output += "[" + c.date + "]\n(" + c.author + ') - ' + c.text + "\n\n"
    return output

##### BOT #####

#@bot.message_handler(commands=['start'])
#def start_handler(message):
#    chat_id = message.chat.id
#    msg = bot.send_message(chat_id, "Hello, potato!")
#
#@bot.message_handler(commands=['posts'])
#def start_handler(message):
#    chat_id = message.chat.id
#
#    output = "POSTS:\n"
#    for p in posts:
#        output = output + "[" + p.date + "]\n(" + p.author + ') - ' + p.text + "\n\n"
#    output = output + "COMMENTS:\n"
#    for c in comments:
#        output = output + "[" + c.date + "]\n(" + c.author + ') - ' + c.text + "\n\n"
#    print(output)
#
#    msg = bot.send_message(chat_id, output)

def parse_rss(link):
    global old_hashes
    feed = feedparser.parse(link)
    hashes = []
    for entry in feed.entries:
        #print(str(entry.link))
        hash = h.md5(entry.link.encode('utf-8')).hexdigest()
        hashes.append(hash)
        if not hash in old_hashes:
            #print(entry.title)
            p_link = entry['links'][0]['href']
            wid, title, post = parse_post(p_link)
            #print(wid, title, post)
            mess = "Post by #" + wid + " - *" + title + "*\n" + post + "\n" + p_link
            #print(mess)
            send_message(mess)
    #print(hashes)
    old_hashes = hashes


#bot.polling(none_stop=True)

#parse_post("https://w41k3r.com/w47k3r5_j01n-playlist-is-updated/")

def send_message(message):
    msg = bot.send_message(channel, message, parse_mode='Markdown', disable_web_page_preview=True)
 #requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}&text={message}')

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    old_hashes = [h.md5("lol".encode('utf-8')).hexdigest()]
    while True:
        parse_rss(rss_link)
        sleep(2)
