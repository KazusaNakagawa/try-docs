import gspread
from google.oauth2.service_account import Credentials
from typing import List

from src.google_api.models.client_service import ClientService


class SheetsApi(ClientService):

    def __init__(self):
        super().__init__()
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
        ]
        self.secret_credentials_json_oath = 'token/gmail-api-355022-service-account-key.json'

    def read_sheet(self, open_by_key=None, sheet_num=0, cell_range='A2:D') -> gspread.worksheet.ValueRange:
        """ SpreedSheet 読み込み

        :param
          open_by_key: Sheet URL
                        https://docs.google.com/spreadsheets/d/{ココ}/edit#gid=0
          sheet_num(int): 読み込みシート番号
          cell_range(str): セル取得範囲

        Sheet: アカウント一覧
        A: No
        B: アカウント名
        C: メールアドレス
        D: zipパスワード

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

    @classmethod
    def read_users(cls, worksheet_data: gspread.worksheet.ValueRange) -> List:
        """ アカウント一覧を取得する

        :param
          worksheet_data: Spread Sheets 参照 セル範囲
        :return:
          users(List): アカウント一覧
        """
        users = []

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

    @classmethod
    def read_mail_templates(cls, worksheet_data: gspread.worksheet.ValueRange) -> List:
        """ メール本文の読み込み

        :param
          worksheet_data: Spread Sheets 参照 セル範囲
        :return:
          mail_tmps(List): メールテンプレ
        """
        mail_tmps = []

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
