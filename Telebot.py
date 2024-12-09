import telebot
from extensions import APIException, СurrencyСonversion
from config import TOKEN, currencies #импортируем константы



bot = telebot.TeleBot(TOKEN) #создаем бота

@bot.message_handler(commands=["start", "help"])
def start_bot(message):
    """Вывод стартового сообщения/помощи"""
    bot.send_message(message.chat.id, f"Приветствую тебя {message.from_user.first_name}! "
                                      f"Я помогу тебе перевести одну валюту в другую, для этого тебе нужно ввести: \n"
                                      f"<имя валюты, цену которой ты хочешь узнать> \n"
                                      f" <имя валюты, в которую нужно перевести первую валюту> <количество первой валюты>. \n"
                                      f"например: 'доллар рубль 100' \n"
                                      f"для получения списка доступных валют введи :/values")


@bot.message_handler(commands=["values"])
def values(message):
    """Вывод сообщения со списком доступных валют """
    text =  ""
    for key in currencies.keys():
        text += key + "\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def currency_conversion(message):
    """Конвертер валют

    Вызов статичного метода класса для проветки правильности введенных данных"""
    try:
        if len(message.text.split()) != 3: # Проверка корректности введенной фразы по длинне
            raise APIException("Не правильно введён запрос.")
        base, quote, amount = message.text.split()

        total = СurrencyСonversion.get_price(base, quote, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f" {e}")
    else:
        bot.send_message(message.chat.id, f" {amount} {base} в {quote}: {total}")



bot.polling(non_stop=True)
