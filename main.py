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
    reply = 'Что-то пошло не так...'
    try:
        _, date, task = message.text.split(maxsplit=2)
    except ValueError:
        reply = 'Введи /add дата задача'
    else:
        date = date.lower()
        if date not in tasks:
            tasks[date] = []
        tasks[date].append(task)
        reply = f'Задача {task}, добавлена на {date}'
    # TODO save task to file
    bot.reply_to(message, reply)


@bot.message_handler(commands=['show', 'print'])
def show(message):
    try:
        split_command = message.text.split()
    except ValueError:
        bot.reply_to(message, 'Введи /show дата')
        return

    dates = split_command[1:]

    # можно вручную не ковырять, ведь выше мы получили список из списка

    # dates = dates.lower()  эта строка у меня вообще выдаёт ошибку:
    # AttributeError: 'list' object has no attribute 'lower', но разбираться я не стал

    # dates_new = str(dates).replace("'", "")
    # dates_new = str(dates_new).replace("[", "")
    # dates_new = str(dates_new).replace("]", "")
    # dates_split = dates_new.split()

    # i = 0  # как уже сказали в чате это лишнее, цикл  for и так присваивает переменной нужное нам значение
    for date in dates:
        date = date.lower()
        if date in tasks:
            reply = f"{date.upper()}\n"
            for task in tasks[date]:
                reply += f"[ ] {task}\n"
        else:
            reply = f"Задач на {date} нет"  # более информативный вывод
            # i += 1
        bot.reply_to(message, reply)


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
