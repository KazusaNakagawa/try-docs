from src.google_api import const
from src.google_api.models.gmail_api import GmailApi
from src.google_api.views import send_gmail_view
from src.google_api.models.zip import Zip
from src.google_api.models.sheets_api import SheetsApi


def send_gmail_attach_file() -> None:
    """ 添付ファイルつき Gmail送信

    :return:
      None
    """
    # user一覧読み込む
    sheets_api = SheetsApi()
    users = sheets_api.read_users()
    # 送信アカウントid 取得
    user_id = send_gmail_view.send_gmail_select_user_console(users)

    # zip圧縮: passつき
    Zip(zip_pass=users[user_id]['zip_pass']).run_zip_compress()

    gmail_api = GmailApi(
        sender=users[user_id]['mail_address'],
        to=users[user_id]['mail_address'],
        zip_dir=const.ZIP_DIR,
        zip_name=const.ZIP_NAME
    )
    # メール本文の作成・送信
    mail_templates = sheets_api.read_mail_templates()
    subject = mail_templates[user_id]['subject']
    message_text = mail_templates[user_id]['mail_text']
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
