import telebot
from secret import TOKEN

HELP = '''
/help - напечатать список команд
/add - добавить задачу в список
/show - напечатать все добавленные задачи.
'''

bot = telebot.TeleBot(TOKEN)

tasks = {}

# def get_command(message):
#     ...


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    bot.reply_to(message, '... add')
#     task = input("Введите задачу: ")
#     date = input("Введите дату: ")
#     if not date in tasks:
#         tasks[date] = []
#     tasks[date].append(task)
#     print(f"Задача {task} добавлена на дату {date}")


@bot.message_handler(commands=['show'])
def show(message):
    bot.reply_to(message, '... show')
    # print(tasks)
    # date = input("Введите дату: ")
    # if date in tasks:
    #     for task in tasks[date]:
    #         print('[ ]', task)
    # else:
    #     print(f'Задач на {date} нет')


@bot.message_handler(content_types=['text'])
def echo_all(message):
    text = ''
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

