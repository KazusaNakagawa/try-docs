from src.google_api import const
from src.google_api.models.gmail_api import GmailApi
from src.google_api.models.sheets_api import SheetsApi
from src.google_api.models.zip import Zip


def send_gmail_attach_file():
    """ 添付ファイルつき Gmail送信 """

    # user一覧読み込む
    sheets_api = SheetsApi()
    users = sheets_api.read_users(
        worksheet_data=sheets_api.read_sheet(const.OPEN_BY_KEY)
    )
    print(users)

    for user in users:
        # zip圧縮: passつき
        Zip(zip_pass=user['zip_pass']).run_zip_compress()

        gmail_api = GmailApi(
            sender=user['mail_address'],
            to=user['mail_address'],
            zip_dir='zip_storage',
            zip_name='sample.zip'
        )
        # メール本文の作成・送信
        subject = 'メール送信自動化テスト_ Class Gmail API'
        message_text = f'メール送信の自動化テストをしています。\n {user}'
        message = gmail_api.create_message_attach_file(subject=subject, message_text=message_text)
        gmail_api.send_message(user_id='me', msg=message)


def send_gmail():
    """ テキスト文のみ Gmail 送信 """
    gmail_api = GmailApi(sender=const.SENDER_ADDRESS, to=const.TO_ADDRESS)

    # メール本文の作成
    subject = 'メール送信自動化テスト_ Class Gmail API'
    message_text = 'メール送信の自動化テストをしています。'
    message = gmail_api.create_message(subject_=subject, msg_text=message_text)

    gmail_api.send_message(user_id='me', msg=message)
