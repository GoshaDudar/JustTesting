import telebot
import COVID19Py
import config

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    send_message = f"Привет {message.from_user.first_name}!\nХочешь узнать последние данные насчёт коронавируса?\nНапиши " \
           f"название страны, пример: США, Украина, Россия..."
    bot.send_message(message.chat.id, send_message, parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    error = False
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "сша":
        location = covid19.getLocationByCountryCode("US")
    elif get_message_bot == "украина":
        location = covid19.getLocationByCountryCode("UA")
    elif get_message_bot == "россия":
        location = covid19.getLocationByCountryCode("RU")
    else:
        bot.send_message(message.chat.id, "Введите верную или другую страну")
        error = True

    if not error:
        final_message = f"<u>Данные по стране:</u>\nКоличество населения: {location[0]['country_population']:,}\nПоследнее обновление: {location[0]['last_updated']}\nПоследние данные:\n<b>Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>{location[0]['latest']['deaths']:,}\n<b>Выздоровели: </b>{location[0]['latest']['recovered']:,}"
        bot.send_message(message.chat.id, final_message, parse_mode='html')


bot.polling(none_stop=True)