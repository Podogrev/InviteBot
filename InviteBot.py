import telebot
import config
import os
from telebot import types
from flask import Flask, request

server = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚔ Я готов!")
    item2 = types.KeyboardButton("🧙‍♂️ О гильдии.")

    markup.add(item1, item2)
    types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id,
                     "Приветствую, {0.first_name}!\nЯ - бот, который добавит тебя в Пермскую "
                     "Гильдию Тестировщиков\nГотов ли ты присоединиться к нам?".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "⚔ Я готов!":
            types.ReplyKeyboardRemove(True)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            link = bot.export_chat_invite_link(chat_id=-372730256)
            item1 = types.KeyboardButton(link)

            markup.add(item1)

        elif message.text == '🧙‍♂️ О гильдии.':
            bot.send_message(message.chat.id, 'QA Guild Perm — активное сообщество тестировщиков, в котором мы '
                                              'делимся своим профессиональным опытом и помогаем друг другу расти.\n\n '
                                              'Будем обсуждать последние тренды и новые инструменты, вместе решать '
                                              'проблемы и коллекционировать мемы. Мы открыты для всех, кому интересно '
                                              'тестирование и обеспечение качества! Присоединяйся и переходи на новый '
                                              'уровень!')

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


# RUN
bot.polling(none_stop=True, timeout=10000)

if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
