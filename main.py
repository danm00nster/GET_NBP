

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Zainstaluj requests
# pip install requests
import requests
import json
from requests.exceptions import HTTPError


def get_rates_of_currency(currency, rates_number):
    try:
        # Skorzystamy z NBP API
        # http://api.nbp.pl/
        url = f'http://api.nbp.pl/api/' \
              f'exchangerates/rates/a/' \
              f'{currency}/' \
              f'last/{rates_number}/' \
              f'?format=json'
        response = requests.get(url)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}')
    except Exception as e:
        print(f'Other exception: {e}')
    else:
        if response.status_code == 200:
            return json.dumps(
                response.json(),
                indent=4,
                sort_keys=True
            )


if __name__ == '__main__':
    currency = 'gbp'
    rates_number = 3
    print(get_rates_of_currency(
        currency,
        rates_number
    ))