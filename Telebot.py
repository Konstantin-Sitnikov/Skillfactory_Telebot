import json

import telebot
import requests
from extensions import APIException
from config import TOKEN, currencies, API #импортируем константы

class СurrencyСonversion:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException("Я не могу перевести одну и ту же валюту")

        if not base.isalpha():
            raise APIException(f"введите название валюты: '{base}' без цифр и знаков препинания! ")

        if not quote.isalpha():
            raise APIException(f"введите название валюты: '{quote}' без цифр и знаков препинания! ")

        if base not in currencies:
            raise APIException(f"я не знаю такой валюты: {base}")

        if quote not in currencies:
            raise APIException(f"я не знаю такой валюты: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Количество валюты: '{amount}' должно быть указанно числом: ")

        try:
            r = requests.get(f"https://v6.exchangerate-api.com/v6/{API}/latest/{currencies[base]}")
        except requests.exceptions.ConnectTimeout:
            raise APIException(f"Превышен тайм-аут соединения.")
        else:
            if r.status_code == 200:
                data = json.loads(r.content)
                return data['conversion_rates'][currencies[quote]] * float(amount)
            else:
                raise APIException(f"данные не получены ошибка {r.status_code}.")




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
    try:
        if len(message.text.split()) != 3:
            raise APIException("Не правильно введён запрос")
        base, quote, amount = message.text.split()

        total = СurrencyСonversion.get_price(base, quote, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f" {e}")
    else:
        bot.send_message(message.chat.id, f" {amount} {base} в {quote}: {total}")



bot.polling(non_stop=True)
