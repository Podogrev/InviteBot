# Initialize DB and functions
import os
import sqlite3


def loadDB():
    # Creates SQLite database to store info.
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''CREATE TABLE IF NOT EXISTS userdata
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    firstname TEXT,
    Name TEXT,
    Organization TEXT,
    Interests TEXT);'''
                      )
    conn.commit()
    conn.close()


def checkUser(update, user_data):
    # Checks if user has visited the bot before
    # If yes, load data of user
    # If no, then create a new entry in database
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    if len(cur.execute('''SELECT id FROM userdata WHERE id = ?        
            ''', (update.message.from_user.id,)).fetchall()) > 0:
        c = cur.execute('''SELECT Name FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Name'] = c[0]
        c = cur.execute('''SELECT Organization FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Organization'] = c[0]
        c = cur.execute('''SELECT Interests FROM userdata WHERE id = ?''', (update.message.from_user.id,)).fetchone()
        user_data['Interests'] = c[0]

        print('Past user')
    else:
        cur.execute('''INSERT OR IGNORE INTO userdata (id, firstname) VALUES (?, ?)''',
                    (update.message.from_user.id, update.message.from_user.first_name,))
        print('New user')
    conn.commit()
    conn.close()


def updateUser(category, text, update):
    # Updates user info as inputted.
    conn = sqlite3.connect('content.sqlite')
    cur = conn.cursor()
    conn.text_factory = str
    # Update SQLite database as needed.
    cur.execute('''UPDATE OR IGNORE userdata SET {} = ? WHERE id = ?'''.format(category), \
                (text, update.message.from_user.id,))
    conn.commit()
    conn.close()


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


# Bot body
import telebot
from flask import Flask
from telebot import types

import config
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

server = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("⚔ Я готов!")
    item2 = types.KeyboardButton("🧙‍♂️ О гильдии")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Приветствую, {0.first_name}!\nЯ - бот, который добавит тебя в Пермскую "
                     "Гильдию Тестировщиков\nГотов ли ты присоединиться к нам?".format(
                         message.from_user), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🧙‍♂️ О гильдии':
            bot.send_message(message.chat.id, 'QA Guild Perm — активное сообщество тестировщиков, в котором мы '
                                              'делимся своим профессиональным опытом и помогаем друг другу расти.\n\n'
                                              'Будем обсуждать последние тренды и новые инструменты, вместе решать '
                                              'проблемы и коллекционировать мемы. Мы открыты для всех, кому интересно '
                                              'тестирование и обеспечение качества! Присоединяйся и переходи на новый '
                                              'уровень!')
        elif message.text == '⚔ Я готов!':
            # Form flow
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("3️")
            item2 = types.KeyboardButton("4️⃣")

            markup.add(item1, item2)
            bot.send_message(message.chat.id,
                                     "Отлично. Докажи мне, что ты не собираешься продвигать криптопирамиды. Сколько будет 2+2?", reply_markup=markup)

        elif message.text == '4️⃣':
            link = bot.export_chat_invite_link(chat_id=config.CHAT_ID)
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('🚀 Присоединиться',
                                               url=link)
            markup.add(item1)

            bot.send_message(message.chat.id,
                             'Такс, ответ верный. Может все таки ты и не бот. Вот '
                             'твоя invite-ссылка!', reply_markup=markup)

            # @bot.message_handler(content_types=['text'])
            # def lalala(message):
            #     if message.chat.type == 'private':
            #         bot.send_message(message.chat.id,
            #                                  'Ok, {}!. Теперь назови компанию, в которой ты работаешь:'.format(message))
            #
            #         @bot.message_handler(content_types=['text'])
            #         def lalala(message):
            #             if message.chat.type == 'private':
            #                 bot.send_message(message.chat.id,
            #                                          'Неплохо. Теперь назови компанию, в которой ты работаешь:')
            #
            #                 @bot.message_handler(content_types=['text'])
            #                 def lalala(message):
            #                     if message.chat.type == 'private':
            #                         bot.send_message(message.chat.id,
            #                          'Понятненько. Последний вопросец. Что тебе сейчас наиболее интересно '
            #                          'в тестировании?')
            #
            #                         @bot.message_handler(content_types=['text'])
            #                         def lalala(message):
            #                             if message.chat.type == 'private':
            #                                 link = bot.export_chat_invite_link(chat_id=config.CHAT_ID)
            #                                 markup = types.InlineKeyboardMarkup(row_width=1)
            #                                 item1 = types.InlineKeyboardButton('🚀 Присоединиться',
            #                                                                            url=link)
            #                                 markup.add(item1)
            #
            #                                 bot.send_message(message.chat.id,
            #                                     'Такс, с бумажной волокитой закончили. Вот '
            #                                     'твоя invite-ссылка!', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Ты Меня потестить решил?😡 Пользуйся кнопками, которые я тебе даю!')





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            bot.send_message(chat_id=config.CHAT_ID,
                             text='У нас пополнение! Добро пожаловать, {0.first_name}, @{1.username}!'
                             .format(call.from_user, call.from_user))

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Заходи скорее!',
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Теперь ты в нашем чатике")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True, timeout=10000)

if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    loadDB()
