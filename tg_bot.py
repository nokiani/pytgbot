
from telebot import types
from telebot.util import quick_markup
import telebot

my_chat_id=463582
token='7114656204:AAFqx6WwMQsz-1XC1IkWw_cZW6sFGD86svM'
bot=telebot.TeleBot(token)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    service_button = types.KeyboardButton(text="Услуги")
    about_button = types.KeyboardButton(text="О нас")
    claim_button = types.KeyboardButton(text="Оставить заявку")
    keyboard.add(service_button, about_button, claim_button)
    bot.send_message(message.chat.id, """\
Добрый день!
Добро пожаловать в ЯГриль!\
""", reply_markup=keyboard)

# Handle all other messages.
# @bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
#     'text', 'location', 'contact', 'sticker'])
# def default_command(message):
#     bot.send_message(message.chat.id, "This is the default command handler.")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)

# @bot.message_handler(commands=['quick'])
# def quick_func(message):
#     markup = quick_markup({
#     'Twitter': {'url': 'https://twitter.com'},
#     'Facebook': {'url': 'https://facebook.com'},
#     'Back': {'callback_data': 'whatever'}
#     }, row_width=3)
#     bot.send_message(message.chat.id, "Инфо о компании", reply_markup=markup)

def send_services(message):
    bot.send_message(message.chat.id, '1. Заказать доставку по телефону')
    bot.send_message(message.chat.id, '2. Заказать доставку по WhatsApp')
    bot.send_message(message.chat.id, '3. Позвонить')

def send_claim(message):
    mes=f'Новая заявка: {message.text}'
    bot.send_message(my_chat_id, mes)
    bot.send_message(message.chat.id, 'Спасибо за заявку!')

# @bot.message_handler(commands=['info'])
def info_func(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Инстаграм", url="https://www.instagram.com/yagrill_astana")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Инфо о компании", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    if message.text.lower() == 'о нас':
      info_func(message)
    if message.text.lower() == 'оставить заявку':
      bot.send_message(message.chat.id, 'Будем рады Вас обслужить! Оставьте свои контактные данные')
      bot.register_next_step_handler(message, send_claim)
    if message.text.lower() == 'услуги':
      send_services(message)


if __name__=='__main__':
  bot.infinity_polling()