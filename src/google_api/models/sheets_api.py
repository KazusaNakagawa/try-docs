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
          E: メールテンプレートNo

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
                'mail_tmp_num': user[4],
            }
            users.append(user)

        return users

    def read_mail_templates(self, user: dict) -> tuple[str, str]:
        """ メール本文の読み込み

        :params
          user(dict)

        Sheet: メールテンプレ
          A: No
          B: 件名
          C: 本文

        :return:
          subject, message_text(tuple): 件名, 本文
        """
        worksheet_data = self._read_sheet(open_by_key=OPEN_BY_KEY, sheet_title='メールテンプレ')

        if not worksheet_data[0] == MAIL_TEMPLATE:
            self.logger.error({
                'msg': 'ColNameError The acquisition column items are different.',
                'cols': worksheet_data[0],
            })
            raise ColNameError

        # 項目行削除
        # Extracts the specified template and assigns letters
        mail_tmp = worksheet_data[int(user['mail_tmp_num'])]
        mail_tmp = {
            'id': mail_tmp[0],
            'subject': mail_tmp[1],
            'mail_text': mail_tmp[2].format(account_name=user['account_name']),
        }
        subject = mail_tmp['subject']
        message_text = mail_tmp['mail_text']

        return subject, message_text
