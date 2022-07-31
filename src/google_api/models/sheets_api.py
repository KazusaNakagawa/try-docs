import gspread
from google.oauth2.service_account import Credentials
from typing import List

from config.log_conf import LogConf
from models.custom_error import ColNameError
from models.client_service import ClientService
from const import (
    ACCOUNT_SHEET_NAME,
    MAIL_TEMPLATE,
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
        self.logger = LogConf().get_logger(__file__)

    def _read_sheet(self, open_by_key=None, sheet_title='アカウント一覧') -> List:
        """ SpreedSheet 読み込み

        :param
          open_by_key: Sheet URL > https://docs.google.com/spreadsheets/d/{target area}/edit#gid=0
          sheet_title(str): シート名

        :return
          取得データ(list)
        """
        credentials = Credentials.from_service_account_file(
            self.secret_credentials_json_oath,
            scopes=self.scopes
        )
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(open_by_key).worksheet(sheet_title)

        return workbook.get_all_values()

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
        worksheet_data = self._read_sheet(open_by_key=OPEN_BY_KEY, sheet_title='アカウント一覧')

        # 項目確認
        if not worksheet_data[0] == ACCOUNT_SHEET_NAME:
            self.logger.error({
                'msg': 'ColNameError The acquisition column items are different.',
                'cols': worksheet_data[0],
            })
            raise ColNameError

        users = []
        # カラム名の要素削除
        worksheet_data.pop(0)
        for user in worksheet_data:
            if '' in user:
                break
            user = {
                'id': user[0],
                'account_name': user[1],
                'mail_address': user[2],
                'zip_pass': user[3],
            }
            users.append(user)

        return users

    def read_mail_templates(self, account_name: str) -> List:
        f""" メール本文の読み込み

        :params
          account_name(str): For account of the text

        Sheet: メールテンプレ
          A: No
          B: 件名
          C: 本文

        :return:
          mail_tmps(List): メールテンプレ
        """
        mail_tmps = []

        worksheet_data = self._read_sheet(open_by_key=OPEN_BY_KEY, sheet_title='メールテンプレ')

        if not worksheet_data[0] == MAIL_TEMPLATE:
            self.logger.error({
                'msg': 'ColNameError The acquisition column items are different.',
                'cols': worksheet_data[0],
            })
            raise ColNameError

        # 項目行削除
        worksheet_data.pop(0)
        for mail_tmp in worksheet_data:
            if '' in mail_tmp:
                break
            mail_tmp = {
                'id': mail_tmp[0],
                'subject': mail_tmp[1],
                'mail_text': mail_tmp[2].format(account_name=account_name),
            }
            mail_tmps.append(mail_tmp)

        return mail_tmps
