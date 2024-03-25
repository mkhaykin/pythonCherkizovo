import logging
from db import add_multi, query_data, DataItem, ResultItem
from datetime import date, datetime
import pandas as pd
from typing import Callable
from itertools import islice
import xlsxwriter
import subprocess, sys

PACK_SIZE = 100

logger = logging.getLogger(__name__)


def open_xlsx(filename: str):
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename])


def date_from_excel(value):
    if type(value) is int:
        return datetime.fromtimestamp((value - 25569) * 86400).date()
    else:
        return value


def import_xlsx(filename: str, sheet_name: str = "sales", callback_msg: Callable = None) -> None:
    logger.info(f"{filename} import start.")
    if callback_msg:
        callback_msg("Reading file ...")

    df = pd.read_excel(
        io=filename,
        sheet_name=sheet_name,
        header=None,
        names=[
            "dt",
            "article",
            "kg",
        ],
        skiprows=1,
        converters={
            "dt": date_from_excel
        },
    )

    logger.info(f"{len(df)} rows from file read")

    if callback_msg:
        callback_msg(f"{len(df)} rows from file read")

    datas = (
        DataItem(
            dt=row.get("dt"),
            article=row.get("article"),
            kg=int(row.get("kg")),
        )
        for _, row in df.iterrows()
    )

    if callback_msg:
        callback_msg(f"Start import data ...")

    logger.info(f"Start import data.")

    count = 0
    pack: list[DataItem]
    while pack := list(islice(datas, PACK_SIZE)):
        if callback_msg:
            callback_msg(f"Import status: {count}/{len(df)}")
        add_multi(pack)
        count += len(pack)

    logger.info(f"{filename} import finish.")

    if callback_msg:
        if count:
            callback_msg(f"Added {count} records.")
        else:
            callback_msg("No record process.")


def export_xlsx(filename: str, date_from: date, date_to: date, callback_msg: Callable = None) -> None:
    logger.info(f"Export to {filename} starts. Date between {date_from} and {date_to}.")

    if callback_msg:
        callback_msg("Query result.")

    data: list[ResultItem] = query_data(date_from, date_to)

    if callback_msg:
        callback_msg("Write data to file.")

    logger.info(f"Write data to file {filename}")

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format(
        {
            "bold": True,
            "align": "left",
            "text_wrap": False,
            "valign": "top",
        }
    )

    # Write title
    worksheet.write(0, 0, f"Данные о продажах за период с {date_from} по {date_to}.", title_format)

    header_format = workbook.add_format(
        {
            "bold": True,
            "align": "center",
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )

    # Write header
    for col_num, (value, width) in enumerate((
            ('Год', 5),
            ('Месяц', 7),
            ('Артикул', 15),
            ('Продажи за период', 10),
            ('Доля к месяцу', 10),
            ('Средние продажи за месяц', 10),
            ('Доля к году', 10),
            ('Средние продажи за год', 10),
    )):
        worksheet.set_column(col_num, col_num, width)
        worksheet.write(1, col_num, value)

    worksheet.set_row(1, height=30, cell_format=header_format)

    worksheet.freeze_panes(2, 0)

    # Write data
    for i, item in enumerate(data, 2):
        worksheet.write(i, 0, item.year)
        worksheet.write(i, 1, item.month)
        worksheet.write(i, 2, item.article)
        worksheet.write(i, 3, item.sales_by_period)
        worksheet.write(i, 4, item.share_by_month)
        worksheet.write(i, 5, item.month_avg_sales)
        worksheet.write(i, 6, item.share_by_year)
        worksheet.write(i, 7, item.year_avg_sales)

    workbook.close()

    logger.info("xlsx export finish")

    if callback_msg:
        callback_msg("Xlsx export finished.")
