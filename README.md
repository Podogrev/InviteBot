# InviteBot
Telegram bot
Дает пользователю анкету, после заполнения которой, приглашает в чат. 
После того как пользовтаель вступит в чат, бот отправляет сообщение с данными из анкеты.

# HOWTO
Запустить на Heroku. Procfile сконфигурирован.

# DONE
- Приветствие с кастомной клавиатурой.
- Формирование ссылки на приглашение.
- Отправка сообщения в общий чат.

# TODO
- Анкета. (Возможно прикрутить SQLite)
- Выгрузку анкет в доку
- Проверку на вступление в чатик. (возможно через флаг в таблице того же SQLite) Можно подглядеть тригер на присоединение к группе у WelcomeBot. Оказалось, что кнопки InlineKeyboardButton не поддерживают одновременно параметры url и callback - а для invitebutton это было бы неплохо.
