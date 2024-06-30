import requests
import xml.etree.ElementTree as ET
from typing import Optional


def get_exchange_rates() -> Optional[list]:
    """Получение данных о валютах"""

    url = 'https://cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url, timeout=10)

    if response.status_code == 200:

        exchange_rates_lst = list()

        root = ET.fromstring(response.text)
        for exchange_data in root:
            num_code = exchange_data.find('NumCode').text
            char_code = exchange_data.find('CharCode').text
            nominal = exchange_data.find('Nominal').text
            name = exchange_data.find('Name').text
            value = exchange_data.find('Value').text
            vunit_retention = exchange_data.find('VunitRate').text

            data = {
                'num_code': num_code,
                'char_code': char_code,
                'nominal': nominal,
                'name': name,
                'value': value,
                'vunit_retention': vunit_retention
            }
            exchange_rates_lst.append(data)

        return exchange_rates_lst if exchange_rates_lst else None

    return None


if __name__ == '__main__':
    print(get_exchange_rates())
