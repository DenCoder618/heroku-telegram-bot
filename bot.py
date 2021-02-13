import os
import telebot
import requests
import bs4 as bs
import telebot
import bs4
#from telebot import types

token = os.environ['TELEGRAM_TOKEN']
login = os.environ['WALKER_LOGIN']
password = os.environ['WALKER_PASSWORD']

main_link = "https://w41k3r.com/"
login_link = "https://w41k3r.com/wp-login.php"
alan_link = "https://w41k3r.com/walkers/?w_id=0"

posts = []
comments = []

#start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#start_markup_btn1 = types.KeyboardButton('w41k3r')
#start_markup_btn2 = types.KeyboardButton('Comments')
#start_markup.add(start_markup_btn1)

class Post:
  def __init__(self, data):
    #if data != '':
    self.author = data.find('span').text
    self.url = data.get('href')
    self.comments = int(data.find('p').text.split(' – ')[0].split()[0])
    self.date = data.find('p').text.split(' – ')[1][10:]
    self.text = data.find('h2').text.split(' - ')[1]
class Comment:
  def __init__(self, data, author):
    #if data != '':
    self.author = author
    self.url = data.get('href')
    self.text = data.find('h2').text[1:-1]
    self.responce = data.find_all('p')[0].text[16:-1]
    self.date = data.find_all('p')[1].text[14:]

def potato_parser():
  c = requests.session()
  initial = c.get(login_link)
  login_data = {"log": login, "pwd": password,
                "rememberme": "forever",
                "redirect_to": main_link,
                "redirect_to_automatic": "1"}
  
  page_login = c.post(login_link, data=login_data)
  print(page_login)
  
  page=c.get(alan_link)
  soup = bs.BeautifulSoup(page.text, features="html.parser")
  main = soup.find('main', {'class': 'body-profile centered'})
  post_data = main.find_all('div')[0].find_all('a')
  comm_data = main.find_all('div')[1].find_all('a')
  
  posts = []
  comments = []
  for p in post_data:
    posts.append(Post(p))
  for c in comm_data:
    comments.append(Comment(c, '#0'))

def format_out():
  output = "POSTS:\n"
  for p in posts:
    output += "[" + p.date + "]\n(" + p.author + ') - ' + p.text + "\n\n"
  output += "COMMENTS:\n"
  for c in comments:
    output += "[" + c.date + "]\n(" + c.author + ') - ' + c.text + "\n\n"
  return output

##### BOT #####

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_handler(message):
  chat_id = message.chat.id
  msg = bot.send_message(chat_id, "Hello, potato!")

@bot.message_handler(commands=['posts'])
def start_handler(message):
  c = requests.session()
  initial = c.get(login_link)
  login_data = {"log": login, "pwd": password,
                "rememberme": "forever",
                "redirect_to": main_link,
                "redirect_to_automatic": "1"}
  
  page_login = c.post(login_link, data=login_data)
  print(page_login)
  
  page=c.get(alan_link)
  soup = bs.BeautifulSoup(page.text, features="html.parser")
  main = soup.find('main', {'class': 'body-profile centered'})
  post_data = main.find_all('div')[0].find_all('a')
  comm_data = main.find_all('div')[1].find_all('a')
  
  posts = []
  comments = []
  for p in post_data:
    posts.append(Post(p))
  for c in comm_data:
    comments.append(Comment(c, '#0'))
    
  print(posts)
  
  #potato_parser()
  chat_id = message.chat.id
  
  output = "POSTS:\n"
  for p in posts:
    output = output + "[" + p.date + "]\n(" + p.author + ') - ' + p.text + "\n\n"
  output = output + "COMMENTS:\n"
  for c in comments:
    output = output + "[" + c.date + "]\n(" + c.author + ') - ' + c.text + "\n\n"
  print(output)
  
  msg = bot.send_message(chat_id, output)
  #msg = bot.send_message(chat_id, posts[0].text)

bot.polling(none_stop=True)
