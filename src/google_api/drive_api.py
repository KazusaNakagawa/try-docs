from googleapiclient.errors import HttpError
from client_service import ClientService


class DriveApi(ClientService):

    def __init__(self):
        super().__init__()
        self.service = self.get_service_drive_v3()

    def read_spreadsheet(self, sheet_name=None, sheet_num=None):
        import gspread
        import json

        from google.oauth2.service_account import Credentials

        # 認証のjsonファイルのパス
        secret_credentials_json_oath = 'token/gmail-api-355022-service-account-key.json'
        # secret_credentials_json_oath = './token/token.json'

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = Credentials.from_service_account_file(
            secret_credentials_json_oath,
            scopes=scopes
        )

        gc = gspread.authorize(credentials)

        # https://docs.google.com/spreadsheets/d/{ココ}/edit#gid=0
        workbook = gc.open_by_key('1gc9jNjiy0NKodT7T3uJKw8wQlnjxl7uUB1H__l83DJo')
        worksheet = workbook.get_worksheet(0)

        # 読み込み
        """ シート: カラム情報
        A: No
        B: アカウント名
        C: メールアドレス
        D: zipパスワード
        """
        users = worksheet.get('A2:D')

        for user in users:
            if len(user) < 4:
                break
            user = {
                'id': user[0],
                'account_name': user[1],
                'mail_address': user[2],
                'zip_pass': user[3],
            }
            # binary_converted = ' '.join(map(bin, bytearray(string, "utf-8")))
            # print("The Binary Represntation is:", binary_converted)
        return users
