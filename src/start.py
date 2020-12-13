import telebot
import property
from .Mode import Mode
import pickle
from .advice import get_joke

bot = telebot.TeleBot(property.token)
moder = Mode()


@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.chat.first_name
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.KeyboardButton(text='Поделиться настроением️')
    btn2 = telebot.types.KeyboardButton(text='Получить совет')
    keybd.add(btn1)
    keybd.add(btn2)
    text = 'Привет, {}! \n \n'.format(name)
    text += "Я твой новый виртуальный друг. Меня зовут Гарри!\nТы всегда можешь обратиться ко мне за советом🤓"
    bot.send_message(message.chat.id, text, reply_markup=keybd)


# Обработчик 0-положения
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.INITIAL_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text

    if text == 'Поделиться настроением️':
        message = "Расскажи в одном предложении о том, что у тебя сейчас на душе"
        moder.mode = Mode.States.RECORDING_STATE
    else:
        bot.send_message(chat_id, 'Мы можем просто поболтать)')
        bot.send_message(chat_id, 'Но у меня ощущение, что у тебя камень на душе')
        message = 'Выговорись - выбери кнопку \'Поделиться настроением\''
    bot.send_message(chat_id, message)


# Обработчик текстовых сообщений или, иначе говоря, 1-состояния
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.RECORDING_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text

    filename = 'data/finalized_model.sav'

    loaded_model = pickle.load(open(filename, 'rb'))

    emo = loaded_model.predict([text])[0]

    if emo == -1:
        message = "Мое бионическое сердце подсказывает, что тебе плохо"
    else:
        message = "Дружок, да ты поди счастлив. Я сделаю твой день еще ярче!"

    # message = get_joke('хорошо') if emo == 1 else get_joke('плохо')
    # bot.send_message(chat_id, 'Мой старый приятель всегда говорил:')
    # bot.send_message(chat_id, message)
    # message = 'правда, порой он несет бред'

    moder.mode = Mode.States.INITIAL_STATE
    bot.send_message(chat_id, message)


bot.polling()
