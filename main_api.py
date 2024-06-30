import json
import os
from datetime import date, datetime
from typing import Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from db_works import DataBase

load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    # allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/get_exchange')
async def get_exchange(response: Response, num_code: str = None, char_code: str = None,
                       date_req: str = None) -> Union[dict, str]:
    """
    Запрос данных о валюте
    прим. - http://127.0.0.1:5000/get_exchange?num_code=036&char_code=AUD&date_req=30.06.2024

    GET запрос, data передается как json в теле запроса.
    :param response:
    :param num_code: Номер валюты
    :param char_code: Код валюты
    :param date_req: Стоимость валюты на определенную дату
    :return: Данные о валюте в json, либо строка с описанием ошибки при составлении запроса
    """

    if not num_code and not char_code:
        # если не указан параметр валюты для запроса
        response.status_code = status.HTTP_400_BAD_REQUEST
        return 'В запросе должен быть указан num_code или char_code'

    if date_req:
        try:
            date_req = datetime.strptime(date_req, "%d.%m.%Y")
        except ValueError:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f'Дата {date_req} указана неверно!'
    else:
        # если дата не передана в запросе, для получения данных из бд используется текущая дата
        date_req = date.today()

    db = DataBase()
    data = db.get_exchange_data(num_code=num_code, char_code=char_code, date=date_req)

    if data:
        exchange = data.get('exchange')
        result = data.get('result')

        if not result:
            response.status_code = status.HTTP_404_NOT_FOUND
            return (f'Данные по валюте {"num_code=" + str(num_code) if num_code else "char_code=" + char_code} '
                    f'за {date_req} отсутствуют')

        response_data = {
            'name': exchange[1],
            'num_code': exchange[2],
            'char_code': exchange[3],
            'value': result[2],
            'vunit_retention': result[3],
            'request_date': result[4].strftime("%d.%m.%Y")
        }
        response_data = json.dumps(response_data, ensure_ascii=False)
        response.status_code = status.HTTP_200_OK
        return response_data
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return 'Данные о валюте отсутствуют'


if __name__ == "__main__":
    host = '0.0.0.0'
    port = int(os.getenv('API_PORT'))
    uvicorn.run("main_api:app", host=host, port=port, log_level="info")
