import datetime

from exchange_rates import get_exchange_rates
from db_works import DataBase


def logic():
    """Логика для получения данных и их сохранения в базу данных"""

    print('Старт получения курсов валют')

    if exchange_rates := get_exchange_rates():

        db = DataBase()

        for item in exchange_rates:
            num_code = item.get('num_code')
            char_code = item.get('char_code')
            nominal = item.get('nominal')
            name = item.get('name')
            value = item.get('value')
            vunit_retention = item.get('vunit_retention')

            exchange_id = db.get_exchange(num_code)
            print(f'{exchange_id=}')

            if not exchange_id:
                print('Сохранение параметров валюты')
                params_for_save = {
                    'num_code': num_code,
                    'char_code': char_code,
                    'nominal': nominal,
                    'name': name
                }
                exchange_id = db.save_exchange_params(params_for_save)
            else:
                exchange_id = exchange_id[0]

            data_for_save = {
                'exchange_id': exchange_id,
                'value': value.replace(',', '.'),
                'vunit_retention': vunit_retention.replace(',', '.'),
                'request_date': datetime.datetime.now()
            }
            db.save_exchange_data(data_for_save)


if __name__ == '__main__':
    logic()
