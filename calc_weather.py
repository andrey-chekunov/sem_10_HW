import telebot

bot = telebot.TeleBot('5620358417:AAHf7gZDicGHSd9lGybIweM0EDpoW9bnF_o')
# value - переменная , в которой будет храниться текущее значение data (калькулятора)
value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton(' ', callback_data='no'),
             telebot.types.InlineKeyboardButton('C', callback_data='C'),
             telebot.types.InlineKeyboardButton('<=', callback_data='<='),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))
keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('*', callback_data='*'))
keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))
keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton(' ', callback_data='no'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton(',', callback_data='.'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=['start', 'calculator', ])
def get_message(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)


# Обработчик событий , который отвечает при нажатии на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    # Теперь data - это то, что возвращает кнопка или то, чему равен аргумент callback_data
    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '=':
        value = str(eval(value))
    else:
        value += data

    if value != old_value:
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id, text='0',
                                  reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id, text=value,
                                  reply_markup=keyboard)
    old_value = value


from pyowm import OWM


def get_location(lat, lon):
    url = f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url


def weather(city: str):
    owm = OWM('3b8fc3bd219841d45de9fdd16dea0946')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = weather.temperature("celsius")
    return temperature, location


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == '/weather':
        bot.send_message(message.from_user.id, "Введите название города: ")
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.from_user.id, "Напишите /weather ")


def get_weather(message):
    city = message.text
    try:
        w = weather(city)
        bot.send_message(message.from_user.id,
                         f'В городе {city} сейчас {round(w[0]["temp"])} градусов, чувствуется как {round(w[0]["feels_like"])} градусов')
        bot.send_message(message.from_user.id, w[1])
        bot.send_message(message.from_user.id, 'Введите название города: ')
        bot.register_next_step_handler(message, get_weather)
    except Exception as e:
        bot.send_message(message.from_user.id, "Такого города нет в базе. Еще разок")
        bot.send_message(message.from_user.id, 'Введите название города: ')
        bot.register_next_step_handler(message, get_weather)
        # print(e)


bot.polling(none_stop=False, interval=0)
