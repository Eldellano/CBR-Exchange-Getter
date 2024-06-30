import json
import requests

# python -m pytest

url = 'http://127.0.0.1:5000/get_exchange'


def test_no_params_api():
    """Проверка api без передачи параметров"""

    res = requests.get(url=url, timeout=10)
    assert res.status_code == 400


def test_with_num_params_api():
    """Проверка api c передачей параметра num_code"""

    params = {
        'num_code': '036'
    }

    res = requests.get(url=url, params=params, timeout=10)
    assert res.status_code == 200


def test_with_char_params_api():
    """Проверка api c передачей параметра char_code"""

    params = {
        'char_code': 'AUD'
    }

    res = requests.get(url=url, params=params, timeout=10)
    assert res.status_code == 200


def test_with_both_params_api():
    """Проверка api c передачей параметров num_code char_code"""

    params = {
        'num_code': '036',
        'char_code': 'AUD'
    }

    res = requests.get(url=url, params=params, timeout=10)
    assert res.status_code == 200


def test_wrong_type_date():
    """Не правильная дата"""

    params = {
        'num_code': '036',
        'char_code': 'AUD',
        'date_req': '30.06.202'
    }
    res = requests.get(url=url, params=params, timeout=10)
    assert res.json() == 'Дата 30.06.202 указана неверно!'


def test_type_answer():
    """Тип данных успешного ответа"""

    params = {
        'num_code': '036',
        'char_code': 'AUD'
    }

    res = requests.get(url=url, params=params, timeout=10)
    if res.status_code == 200:
        json_response = json.loads(res.json())

        assert isinstance(json_response, dict)


def test_with_wrong_char_params_api():
    """Проверка api c передачей параметра char_code"""

    params = {
        'char_code': 'PYT'
    }

    res = requests.get(url=url, params=params, timeout=10)
    assert res.status_code == 404


def test_wrong_date():
    """Не правильная дата"""

    params = {
        'num_code': '036',
        'char_code': 'AUD',
        'date_req': '30.06.2022'
    }
    res = requests.get(url=url, params=params, timeout=10)
    assert res.status_code == 404
