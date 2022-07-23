import gspread
from google.oauth2.service_account import Credentials
from typing import List

from src.google_api.models.client_service import ClientService
from src.google_api.const import (
    OPEN_BY_KEY,
    SECRET_CREDENTIALS_JSON_OATH,
)


class SheetsApi(ClientService):

    def __init__(self):
        super().__init__()
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
        ]
        self.secret_credentials_json_oath = SECRET_CREDENTIALS_JSON_OATH

    def _read_sheet(self, open_by_key=None, sheet_num=0, cell_range='A2:D') -> gspread.worksheet.ValueRange:
        """ SpreedSheet 読み込み

        :param
          open_by_key: Sheet URL > https://docs.google.com/spreadsheets/d/{target area}/edit#gid=0
          sheet_num(int): 読み込みシート番号
          cell_range(str): セル取得範囲

        :return
          取得データ: (gspread.worksheet.ValueRange)
        """
        credentials = Credentials.from_service_account_file(
            self.secret_credentials_json_oath,
            scopes=self.scopes
        )
        gc = gspread.authorize(credentials)

        workbook = gc.open_by_key(open_by_key)
        worksheet = workbook.get_worksheet(sheet_num)

        return worksheet.get(cell_range)

    def read_users(self) -> List:
        """ アカウント一覧を取得する

        Sheet: アカウント一覧
          A: No
          B: アカウント名
          C: メールアドレス To
          D: zipパスワード

        :return:
          users(List): アカウント一覧
        """
        users = []

        worksheet_data = self._read_sheet(open_by_key=OPEN_BY_KEY)

        for user in worksheet_data:
            if len(user) < 4:
                break
            user = {
                'id': user[0],
                'account_name': user[1],
                'mail_address': user[2],
                'zip_pass': user[3],
            }
            users.append(user)

        return users

    def read_mail_templates(self) -> List:
        """ メール本文の読み込み

        Sheet: メールテンプレ
          A: No
          B: 件名
          C: 本文

        :return:
          mail_tmps(List): メールテンプレ
        """
        mail_tmps = []

        worksheet_data = self._read_sheet(open_by_key=OPEN_BY_KEY, sheet_num=1, cell_range='A2:C')

        for mail_tmp in worksheet_data:
            if len(mail_tmp) < 3:
                break
            mail_tmp = {
                'id': mail_tmp[0],
                'subject': mail_tmp[1],
                'mail_text': mail_tmp[2],
            }
            mail_tmps.append(mail_tmp)

        return mail_tmps
