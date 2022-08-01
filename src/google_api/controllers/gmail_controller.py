import const
from models.gmail_api import GmailApi
from views import (
    send_gmail_gui,
    select_file_gui,
)
from models.zip import Zip
from models.sheets_api import SheetsApi


def send_gmail_attach_file() -> None:
    """ 添付ファイルつき Gmail送信

    :return:
      None
    """
    # user一覧読み込む
    sheets_api = SheetsApi()
    users = sheets_api.read_users()
    # 送信アカウントid 取得
    user_id = send_gmail_gui.select_send_gmail_gui(users)

    # 添付ファイル選択
    attach_file = select_file_gui.select_file_gui()

    # zip圧縮: passつき
    # Zip(zip_pass=users[user_id]['zip_pass']).run_zip_compress()

    gmail_api = GmailApi(
        sender=users[user_id]['mail_address'],
        to=users[user_id]['mail_address'],
    )
    # メール本文の作成・送信
    mail_templates = sheets_api.read_mail_templates(account_name=users[user_id]['account_name'])
    subject = mail_templates[user_id]['subject']
    message_text = mail_templates[user_id]['mail_text']
    message = gmail_api.create_message_attach_file(
        attach_file_path=attach_file, subject=subject, message_text=message_text
    )
    gmail_api.send_message(user_id='me', msg=message)


def send_gmail():
    """ テキスト文のみ Gmail 送信 """
    gmail_api = GmailApi(sender=const.SENDER_ADDRESS, to=const.TO_ADDRESS)

    # メール本文の作成
    subject = 'メール送信自動化テスト_ Class Gmail API'
    message_text = 'メール送信の自動化テストをしています。'
    message = gmail_api.create_message(subject_=subject, msg_text=message_text)

    gmail_api.send_message(user_id='me', msg=message)
