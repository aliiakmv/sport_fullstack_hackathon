import telebot
from telebot import types
import peewee
from parser import *

URL = 'https://www.google.com/maps/search/%D1%81%D0%BF%D0%BE%D1%80%D1%82+%D0%B7%D0%B0%D0%BB%D1%8B+%D0%B1%D0%B8%D1%88%D0%BA%D0%B5%D0%BA%D0%B5/@42.8507109,74.5766912,14z/data=!3m1!4b1'

bot = telebot.TeleBot('5846294059:AAH1CLO6RhlRqxuEnWFEi1XlsUzfNAt2Cak')

html = get_sports_sections_html(url=URL)
soup = get_soup(html)
data = get_data(soup)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Site')
    btn3 = types.KeyboardButton('Gym')
    btn2 = types.KeyboardButton('Subscription')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}!".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Site':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Спорт сайт", url='http://34.125.95.67/')
        markup.add(button1)
        bot.send_message(message.chat.id,
                         "Здравствуйте, {0.first_name}! Нажми на кнопку и перейди на наш сайт)".format(
                             message.from_user),
                         reply_markup=markup)
    elif message.text == 'Subscription':
        bot.send_message(message.chat.id,
                         'Здравствуйте! \nМы можем предложить Вам выгодные абонементы на любой спортзал находящийся в Бишкеке: \n\n  Абонемент на 730 дней Вам обойдется за 80 000 сом \n  Абонемент на 365 дней Вам обойдется за 50 000 сом \n  Абонемент на 180 дней Вам обойдется за 35 000 сом \n  Абонемент на 90 дней Вам обойдется за 20 000 сом ')
    elif message.text == 'Gym':
        for i in data[:5]:
            bot.send_message(message.chat.id, i)


bot.polling()
