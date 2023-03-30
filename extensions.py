import requests
import json
from config import API_URL, API_KEY

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Нельзя перевести одинаковые валюты: {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}.')

        url = f"{API_URL}/v6/convert?q={base}_{quote}&compact=ultra&apiKey={API_KEY}"
        response = requests.get(url)
        data = json.loads(response.text)

        if not data:
            raise APIException(f'Не удалось получить курс для валюты: {base}_{quote}')

        exchange_rate = data[f"{base}_{quote}"]
        result = exchange_rate * amount
        return result
