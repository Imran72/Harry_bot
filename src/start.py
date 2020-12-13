import telebot
import property
from .Mode import Mode
import pickle

bot = telebot.TeleBot(property.token)
moder = Mode()


@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.chat.first_name
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn3 = telebot.types.KeyboardButton(text='Поделиться настроением️')
    keybd.add(btn3)
    text = 'Привет, {}! \n \n'.format(name)
    text += "Я твой новый виртуальный друг. Меня зовут Гарри!\nТы всегда можешь обратиться ко мне за советом🤓"
    bot.send_message(message.chat.id, text, reply_markup=keybd)


# Обработчик 0-положения
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.INITIAL_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text

    message = ""

    if text == 'Поделиться настроением️':
        message = "Расскажи в одном предложении о том, что у тебя сейчас на душе."
        moder.mode = Mode.States.RECORDING_STATE
    bot.send_message(chat_id, message)


# Обработчик текстовых сообщений или, иначе говоря, 1-состояния
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.RECORDING_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text

    filename = 'finalized_model.sav'

    loaded_model = pickle.load(open(filename, 'rb'))

    emo = loaded_model.predict([text])[0]

    if emo == -1:
        message = "Мое бионическое сердце подсказывает, что тебе плохо"
    else:
        message = "Дружок, да ты поди счастлив. Я сделаю твой день еще ярче!"

    moder.mode = Mode.States.INITIAL_STATE
    bot.send_message(chat_id, message)

bot.polling()
