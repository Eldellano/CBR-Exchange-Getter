import datetime
import os

from sqlalchemy import create_engine, select, insert, or_, and_

from models import ExchangeParams, ExchangeData


class DataBase:
    def __init__(self):
        self.postgres_host = os.getenv('POSTGRES_HOST')
        self.postgres_port = os.getenv('POSTGRES_PORT')
        self.postgres_db = os.getenv('POSTGRES_DB')
        self.postgres_user = os.getenv('POSTGRES_USER')
        self.postgres_pass = os.getenv('POSTGRES_PASS')

        self.engine = create_engine(
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_pass}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}",
            isolation_level="AUTOCOMMIT",
            pool_pre_ping=True,
        )

    def save_exchange_params(self, exchange_params):
        """Добавление параметров валюты"""

        query = insert(ExchangeParams).values(exchange_params).returning(ExchangeParams.id)

        with self.engine.connect() as conn:
            result = conn.execute(query).fetchone()[0]
            return result

    def save_exchange_data(self, exchange_params):
        """Добавление стоимости валюты"""

        query = insert(ExchangeData).values(exchange_params)

        with self.engine.connect() as conn:
            conn.execute(query)

    def get_exchange(self, num_code: str = None, char_code: str = None):
        """Получение id валюты из таблицы"""

        query = select(ExchangeParams).where(or_(
            ExchangeParams.num_code == num_code,
            ExchangeParams.char_code == char_code
        ))
        with self.engine.connect() as conn:
            result = conn.execute(query).fetchone()

            return result

    def get_exchange_data(self, num_code: str = None, char_code: str = None, date: datetime = None):
        """Получение данных о стоимости валюты через api"""

        exchange = self.get_exchange(num_code, char_code)

        if exchange:
            exchange_id = exchange[0]

            query = select(ExchangeData).where(and_(
                ExchangeData.exchange_id == exchange_id,
                ExchangeData.request_date == date
            ))

            with self.engine.connect() as conn:
                result = conn.execute(query).fetchone()
                return {
                    "exchange": exchange,
                    "result": result
                }


if __name__ == '__main__':
    db = DataBase()
    data = {'num_code': '072', 'char_code': 'AUD', 'nominal': '1', 'name': 'Австралийский доллар'}
    # print(db.save_exchange_params(data))

    # print(db.get_exchange_id(num_code='015'))
    # print(db.get_exchange_id(char_code='AUD'))

    db.get_exchange_data(num_code='036', date='2024-06-29')
