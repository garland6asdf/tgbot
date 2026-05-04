import logging
import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()

URL = 'https://v6.exchangerate-api.com/v6/'
MONEYS = ('USD', 'EUR', 'RUB', 'JPY', 'GBP', 'CNY', 'CAD', 'AUD')
API_TOKEN = os.getenv('API_TOKEN')

def send_request(url, currency):
    """Отправляет запрос к серверу."""
    try:
        endpoint = url + API_TOKEN + currency
        logging.info('trying to get response from server...')
        response = requests.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()
    except (requests.exceptions.RequestException, TypeError) as error:
        logging.error(f'connection error. Error - {error}')


def check_response(response):
    """Проверяет формат ответа и наличие ключей."""
    if not isinstance(response, dict):
        raise TypeError(f'expected type - dict, received - {type(response)}')
    result = response.get('result')
    if not result:
        raise KeyError('key "result" was not found')
    if result != 'success':
        raise ValueError('key "result" != "success"')
    logging.info('format is correct')
    return response.get('conversion_rates')


def parse(conversion_rates):
    """Парсит нужный ключ."""
    if not isinstance(conversion_rates, dict):
        raise TypeError(f'expected type - dict, received - {type(conversion_rates)}')
    result = ''
    try:
        for currency in MONEYS:
            result += f'{currency} - {conversion_rates[currency]}\n'
        return result
    except Exception as error:
        logging.error(f'some error {error}')


def main(currency):
    """Основной код."""
    logging.basicConfig(
    level=logging.INFO,
    format=(
        '%(asctime)s, %(levelname)s, '
        '%(filename)s:%(lineno)d, %(message)s'
    ),
    )
    try:
        response = send_request(URL, currency=currency)
        conversion_rates = check_response(response)
        result = parse(conversion_rates)
        return result
    except Exception as error:
        logging.error(f'Error: {error}')


if __name__ == '__main__':
    main()