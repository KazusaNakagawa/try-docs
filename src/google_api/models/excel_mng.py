import glob
import os
from typing import Literal
import pandas as pd
from openpyxl import load_workbook


def read_excel_file(func):
    def wrapper(*args, **kwargs):
        wb = load_workbook(filename=kwargs['file'], read_only=True)
        print(f"\n{'*' * 10} {kwargs['file']} {'*' * 10}")
        return func(wb)

    return wrapper


@read_excel_file
def show_row_count(wb, col_name: str) -> (int or Literal[False]):
    """指定項目のカウント数を返す

    params:
      wb(object): Workbook
      col_name(str): target Column Name
    return:


    """
    for sheet in wb.sheetnames:
        data = list(wb[sheet].values)
        # Define one row name as a column name
        df = pd.DataFrame(data[1:], columns=data[0])

        for item in list(df.columns):
            print(f" [{item}] row_count: {df[item].count()}")
            if item == col_name:
                return df[item].count()
        return False


if __name__ == '__main__':
    files = glob.glob("../zip_storage/*.xlsx")
    if not files:
        files = glob.glob("./zip_storage/*.xlsx")

    for file in files:
        count = show_row_count(file=file, col_name='項目2')
        print('result:', count)
