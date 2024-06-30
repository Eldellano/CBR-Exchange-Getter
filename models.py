import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Date, String, Integer, Float, Column, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()


class Base(DeclarativeBase):
    pass


class ExchangeParams(Base):
    """Данные о валюте"""

    __tablename__ = 'exchange'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))
    num_code: Mapped[str] = mapped_column(String(length=3))
    char_code: Mapped[str] = mapped_column(String(length=3))
    nominal: Mapped[int] = mapped_column(Integer())


class ExchangeData(Base):
    """Данные о стоимости валюты"""

    __tablename__ = 'exchange_data'
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = Column(Integer, ForeignKey('exchange.id'))
    value: Mapped[float] = mapped_column(Float())
    vunit_retention: Mapped[float] = mapped_column(Float())
    request_date: Mapped[datetime] = mapped_column(Date(), nullable=False)


def migrate():
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT')
    postgres_db = os.getenv('POSTGRES_DB')
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_pass = os.getenv('POSTGRES_PASS')

    engine = create_engine(
        f"postgresql+psycopg2://{postgres_user}:{postgres_pass}@{postgres_host}:{postgres_port}/{postgres_db}",
        isolation_level="SERIALIZABLE"
    )

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    migrate()
