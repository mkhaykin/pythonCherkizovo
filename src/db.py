import pyodbc
from settings import settings
from datetime import date
from dataclasses import dataclass
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)


@dataclass
class DataItem:
    dt: date
    article: str
    kg: int


@dataclass
class ResultItem:
    year: int
    month: int
    article: str
    sales_by_period: int
    year_avg_sales: int
    share_by_year: Decimal
    month_avg_sales: int
    share_by_month: Decimal


connectionString = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={settings.MSSQL_SERVER};'
    f'DATABASE={settings.MSSQL_DATABASE};'
    f'UID={settings.MSSQL_USERNAME};'
    f'PWD={settings.MSSQL_PASSWORD};'
    'TrustServerCertificate=yes;'
)
conn = pyodbc.connect(connectionString)


def add_multi(datas: list[DataItem]) -> None:
    sql_query = (
        "INSERT INTO [sales] (dt, article, kg) "
        "VALUES (?, ?, ?)"
    )
    # TODO try | except
    cursor = conn.cursor()
    lst = [(item.dt.strftime("%Y-%m-%d"), item.article, item.kg) for item in datas]

    cursor.executemany(sql_query, lst)
    cursor.commit()
    cursor.close()


# def add_data(data: DataItem) -> None:
#     sql_query = (
#         "INSERT INTO [sales] (dt, article, kg) "
#         "VALUES (?, ?, ?)"
#     )
#     # TODO try | except
#     cursor = conn.cursor()
#     cursor.execute(sql_query, data.dt, data.article, data.kg)
#     cursor.commit()
#     cursor.close()


def query_data(date_from: date, date_to: date) -> list[ResultItem]:
    sql_query = "exec sp_test ?, ?"

    # TODO try | except
    cursor = conn.cursor()
    cursor.execute(sql_query, date_from, date_to)
    result = [ResultItem(*item) for item in cursor.fetchall()]
    cursor.close()

    return result
