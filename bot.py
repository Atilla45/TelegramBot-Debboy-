
import telegram
import requests
from bs4 import BeautifulSoup
import cssutils
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
import sqlite3
from tabulate import tabulate
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging


response = requests.get('https://oxu.az/')
text = response.text
soup = BeautifulSoup(text, "html.parser")

update_id = None
#
updater = Updater(token='1168292465:AAEILU91gMAKwBue07X1VJxe5oNlXPg4liU')


class SmartBot():
    not_sended = True
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def __init__(self):
        token = '1168292465:AAEILU91gMAKwBue07X1VJxe5oNlXPg4liU'
        self.bot = telegram.Bot(token)
        try:
            bot_update = self.bot.get_updates()
            self.update_id = bot_update[0].update_id
        except IndexError:
            self.update_id = None

        while True:
            try:
                self.echo()
            except NetworkError:
                sleep(1)
            except Unauthorized:
                # The user has removed or blocked the bot.
                self.update_id += 1
            except UnicodeEncodeError:
                self.bot.sendMessage(chat_id=self.chat_id,
                                     text="Sorry, but I can't summarise your text.")

    def exchange(self):
        res = ''
        exchanges = requests.get(
            'https://api.exchangeratesapi.io/latest').json()['rates']
        for x, y in exchanges.items():
            res += f'{x} : {y} \n'

        return res

    def weather(self, city):
        res = ''
        search_city = city
        # object = self.update.message.text
        link = f'https://api.openweathermap.org/data/2.5/weather?q={search_city}&appid=ac5085a3a9b83bee98e37d2fcb1df095'
        response = requests.get(link).json()
        for x, y in response.items():
            res += f'{x} {y} \n'
        return res

    def news(self):
        news_content = soup.findAll("a", {"class": "news-i-inner"})
        konteks = ''

        for x in news_content:
            basliq = x.find_all("div", {"class": "news-i-content"})
            div_style = soup.find('div', {"class": "news-i-img"})['style']
            style = cssutils.parseStyle(div_style)
            topic = basliq[0].text
            url = style['background-image']
            lin = 'https://oxu.az'
            a = x.get('href')
            konteks += topic+'\n'+lin+a+'\n'
            # bot.sendPhoto(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
        print(konteks)
        print(url)
        return konteks

    def find(self, word):

        with open("responses.txt", 'a+') as f:
            result = ''

            f.seek(0)
            # newcall = ''
            sual = f.readlines()
            for i in sual:
                text1 = i.split('::')[0]
                text2 = i.split('::')[1]
                if word == text1:
                    return text2
            else:
                return 'I do not understand ,could you teach me? (yes/no)'

    def start(self):
        self.bot.send_message(
            chat_id=self.chat_id, text='Hi, I am Debboy.Please, register( write: register)')

    def register(self, update):
        self.bot.send_chat_action(
            chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
        self.bot.send_message(
            chat_id=self.chat_id, text='Enter your details in the following format : ''Name, Address, Phone number')

    def checkDetails(self, update):
        connection = sqlite3.connect('userDetails.db', check_same_thread=False)
        value = self.chat_id
        print("VALUE : ", value)
        for row in connection.execute("SELECT *from userdetails WHERE user_id=?", (value,)):
            print(row)
            user_id, customer_name, address, phone_number = row
        labels = ["Customer Name : ", "Address : ", "Phone Number : "]
        data = [customer_name, address, phone_number]
        table = zip(labels, data)
        list = tabulate(table, tablefmt="fancy_grid")
        self.bot.send_message(chat_id=self.chat_id, text=list)

    def database(self, user_id, customer_name, address, phone_number):
        print(user_id, customer_name, address, phone_number)
        connection.execute(
            '''CREATE TABLE IF NOT EXISTS userdetails(user_id int,customer_name text,address text,phone_number int )''')
        connection.execute("INSERT INTO userdetails VALUES (?,?,?,?)",
                           (self.user_id, customer_name, address, phone_number))
        connection.commit()

    def google(self, search_word):
        search_word = search_word
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
        link = f'https://www.google.com/search?q={search_word}'
        headers = {"user-agent": USER_AGENT}
        response = requests.get(link, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        search_result = soup.select('.r a')
        search_result = soup.find_all('div', {'class': 'r'})
        res = ''
        num = 0
        for a in search_result:
            search_text = soup.find_all('h3', {'class': 'LC20lb DKV0Md'})
            search_result_link = soup.select('.r a')
            or_headers = search_text[num].text
            for i in search_result_link:
                or_link = i.get('href')
            res += or_headers + '\n'+or_link+'\n'
            num += 1
        return res

    def cavab(self, request):
        with open("responses.txt", 'a+') as f:
            f.write(request+'\n')

    def echo(self):
        global update_id

        for update in self.bot.get_updates(offset=self.update_id, timeout=30):
            self.update_id = update.update_id + 1
            self.chat_id = update.message.chat_id

            if self.chat_id and self.not_sended:
                reply_markup = telegram.ReplyKeyboardRemove()
                self.bot.send_message(
                    chat_id=self.chat_id, text="I'm back.", reply_markup=reply_markup)
                self.not_sended = False
            if update.message and update.message.text:
                message_text = update.message.text
                # if update.message.text=='he':
                #     update.message.reply_text('elave et')

                #     update.message.reply_text(self.cavab(
                #         update.message.text.strip(' ')))

                # print('start' in message_text.lower())

                if 'cat' in message_text.lower():
                    # print(update.message.chat_id)
                    self.bot.send_chat_action(
                        chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
                    sticker = requests.get(
                        'https://api.thecatapi.com/v1/images/search').json()[0]['url']
                    self.bot.send_sticker(
                        chat_id=self.chat_id, sticker=sticker)
                elif 'start' in message_text.lower():
                    self.start()
                elif 'register' in message_text.lower():

                    update.message.reply_text(self.register('n'))

                elif 'Weather information about' in message_text.lower():

                    update.message.reply_text(self.weather(
                        message_text.lower().replace('hava haqqinda melumat', '').strip(' ')))
                    update.message.reply_text('This is weather information about'+message_text.lower(
                    ).replace('hava haqqinda melumat', '').strip(' '))

                elif 'yes' in message_text.lower():
                    update.message.reply_text(
                        'Please,enter like question::answer')

                elif '::' in message_text.lower():
                    update.message.reply_text(self.cavab(
                        message_text.lower().strip(' ')))

                elif 'search' in message_text.lower():
                    update.message.reply_text('results of your search')
                    update.message.reply_text(self.google(
                        message_text.lower().replace('search', '').strip(' ')))

                elif 'bot' in message_text.lower():
                    update.message.reply_text(self.find(
                        message_text.lower().replace('bot', '').strip(' ')))
                    # if message_text.lower()=='he':
                    #     cavab()

                elif 'checkdetails' in message_text.lower():
                    update.message.reply_text(self.checkDetails('s'))

                elif 'necesen' in message_text.lower():
                    keyboard = [
                        [InlineKeyboardButton("Happy", callback_data='1'),
                            InlineKeyboardButton("Whatever", callback_data='2')],
                        [InlineKeyboardButton("Sad", callback_data='3')]]

                    reply_markup = InlineKeyboardMarkup(keyboard)

                    update.message.reply_text(
                        'Hey there! How do you feel today?', reply_markup=reply_markup)

                    update.message.reply_text(self.search(
                        message_text.lower().replace('bot', '').strip(' ')))

                elif 'news of today' in message_text.lower():
                    update.message.reply_text(self.news())
                    update.message.reply_text(
                        'If you find your search ,click on the link..')

                elif 'send location' in message_text:
                    location_keyboard = telegram.KeyboardButton(
                        text="send_location", request_location=True)
                    contact_keyboard = telegram.KeyboardButton(
                        text="send_contact", request_contact=True)
                    custom_keyboard = [[location_keyboard, contact_keyboard]]
                    reply_markup = telegram.ReplyKeyboardMarkup(
                        custom_keyboard)
                    self.bot.send_message(
                        chat_id=self.chat_id, text="Would you mind sharing your location and contact with me?", reply_markup=reply_markup)
                elif '2' in message_text:
                    self.bot.send_message(chat_id=self.chat_id,
                                          text="*bold* _italic_ `fixed width font` [Facebook](http://google.com)\.", parse_mode=telegram.ParseMode.MARKDOWN_V2)

                elif 'Exchange' in message_text.lower():

                    update.message.reply_text(
                        'Bugunun mezennesi')
                    self.bot.send_chat_action(
                        chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
                    update.message.reply_text(self.exchange())


if __name__ == '__main__':
    SmartBot()
