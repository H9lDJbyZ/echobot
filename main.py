# -*- coding: utf-8 -*-
import telebot
from secret import TOKEN
import requests

HELP = '''
/help - напечатать список команд
/add дата задача - добавить задачу в список
/show дата - напечатать все добавленные задачи
/weather город - погода в городе
'''

bot = telebot.TeleBot(TOKEN)

tasks = {}


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    # mes = message.text.lower()
    _, date, task = message.text.split(maxsplit=2)
    date = date.lower()
    if date not in tasks:
        tasks[date] = []
    tasks[date].append(task)
    reply = f'Задача {task}, добавлена на {date}'
    # TODO add task to file
    bot.reply_to(message, reply)


@bot.message_handler(commands=['show'])
# def show(message):
#     reply = ''
#     # date = 'сегодня'
#     try:
#         date = message.text.split()[1]
#         date.lower()
#     except IndexError:
#         reply = 'Введи /show дата'
#     else:
#         if date in tasks:
#             for task in tasks[date]:
#                 reply += f'[ ] {task}\n'
#         else:
#             reply = f'Задач на {date} нет'
#     bot.reply_to(message, reply)
def show(message):
    reply = 'Что-то пошло не так'  # инициализируем ответ, на всякий случай
    split_command = message.text.split()
    dates = split_command[1:]

    # можно вручную не ковырять, ведь выше мы получили список из списка
    # dates = dates.lower()  # эта строка выдаёт ошибку AttributeError: 'list' object has no attribute 'lower'
    # dates_new = str(dates).replace("'", "")
    # dates_new = str(dates_new).replace("[", "")
    # dates_new = str(dates_new).replace("]", "")
    # dates_split = dates_new.split()

    # i = 0
    for date in dates:
        date = date.lower()
        if date in tasks:
            reply = date.upper() + "\n"
            for task in tasks[date]:
                reply += f"[ ] {task}\n"
        else:
            reply = f"Задач на {date} нет"  # более информативный вывод
            # i += 1
        # print(reply)
        bot.reply_to(message, reply)
    # return reply


@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        city = message.text.split()[1]
    except IndexError:
        reply = 'Введи /weather город'
    else:
        params = {'M': '', 'format': '4', 'lang': 'ru'}
        url = f'https://wttr.in/{city}'
        response = requests.get(url, params)
        reply = response.text
    bot.reply_to(message, reply)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.reply_to(message, message.text)


def main():
    print(f'bot started')
    # TODO read tasks from file
    # f = file('tasks.txt', 'r')
    bot.polling(none_stop=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('bot stopped')
