# -*- coding: utf-8 -*-
import telebot
from secret import TOKEN

HELP = '''
/help - напечатать список команд
/add дата задача - добавить задачу в список
/show дата - напечатать все добавленные задачи.
'''

bot = telebot.TeleBot(TOKEN)

tasks = {}


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    # text = ''
    date, task = message.text.split(maxsplit=2)
    if date not in tasks:
        tasks[date] = []
    tasks[date].append(task)
    text = f'Задача {task}, добавлена на {date}'
    bot.reply_to(message, text)


@bot.message_handler(commands=['show'])
def show(message):
    text = ''
    try:
        date = message.text.split()[1]
    except IndexError:
        text = 'Введи дату'
    else:
        if date in tasks:
            for task in tasks[date]:
                text += f'[ ] {task}\n'
        else:
            text = f'Задач на {date} нет'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    # text = ''
    if '111' in message.text:
        text = '999 ' + message.text
    else:
        text = message.text
    bot.reply_to(message, text)


if __name__ == "__main__":
    try:
        print('bot started')
        bot.polling()
    except KeyboardInterrupt:
        print('bot stopped')
