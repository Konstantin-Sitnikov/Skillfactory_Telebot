import requests
import json
from config import currencies, API




class СurrencyСonversion:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException("Нельзя перевести одинаковую валюту")

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

class APIException(Exception):
    pass