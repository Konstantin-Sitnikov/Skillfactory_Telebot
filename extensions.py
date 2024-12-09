import requests
import json
from config import currencies, API


class СurrencyСonversion:
    """Собственный клас со статичным методом, для проверки корректности введенных данных
    выполнения запроса по API, и расчета итогового значения конвертируемой валюты.

    Выполненые проверки:
    1. Пользователь ввел разные валюты;
    2, 3. Валюты введены без цифр и знаков препинания;
    4, 5. Валют есть в списке валют
    6. Количество валюты введено числом, без букв и символов
    7. Наличие соединения с сервером API (время от времени происходит тайм-аут соединения)
    8. Проверка успешной загрузки данных от API (Если код 200 данные загружены успешно выполняется парсинг через
    библиотеку JSON, и метод возвращает итоговое значение конвертируемой валюты.)

    в случае невыполнения одного из условий пользователю выводится сообщение о соответствующей ошибке

    """
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> any:
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException("Нельзя перевести одинаковую валюту") # 1.

        if not base.isalpha():
            raise APIException(f"введите название валюты: '{base}' без цифр и знаков препинания! ") # 2.

        if not quote.isalpha():
            raise APIException(f"введите название валюты: '{quote}' без цифр и знаков препинания! ") # 3.

        if base not in currencies:
            raise APIException(f"я не знаю такой валюты: {base}") # 4.

        if quote not in currencies:
            raise APIException(f"я не знаю такой валюты: {quote}") # 5.

        try: # 6.
            amount = float(amount)
        except ValueError:
            raise APIException(f"Количество валюты: '{amount}' должно быть указанно числом: ")

        try: # 7.
            r = requests.get(f"https://v6.exchangerate-api.com/v6/{API}/latest/{currencies[base]}")
        except requests.exceptions.ConnectTimeout:
            raise APIException(f"Превышен тайм-аут соединения.")
        else: # 8.
            if r.status_code == 200:
                data = json.loads(r.content)
                return data['conversion_rates'][currencies[quote]] * float(amount)
            else:
                raise APIException(f"данные не получены ошибка {r.status_code}.")


class APIException(Exception):
    """Собственный клас для обработки исключений"""
    pass