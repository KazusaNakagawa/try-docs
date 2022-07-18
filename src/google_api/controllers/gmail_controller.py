from src.google_api import const
from src.google_api.models.gmail_api import GmailApi
from src.google_api.models.sheets_api import SheetsApi
from src.google_api.models.zip import Zip


def send_gmail_attach_file(user_id=1) -> None:
    """ 添付ファイルつき Gmail送信

    :param
      user_id(int): スプレッドシート参照 No
    :return:
      None
    """
    # 参照レコード調整: 2行目から開始している
    user_id = user_id - 1

    # user一覧読み込む
    sheets_api = SheetsApi()
    users = sheets_api.read_users(
        worksheet_data=sheets_api.read_sheet(open_by_key=const.OPEN_BY_KEY)
    )

    # zip圧縮: passつき
    Zip(zip_pass=users[user_id]['zip_pass']).run_zip_compress()

    gmail_api = GmailApi(
        sender=users[user_id]['mail_address'],
        to=users[user_id]['mail_address'],
        zip_dir='zip_storage',
        zip_name='sample.zip'
    )
    # メール本文の作成・送信
    mail_templates = sheets_api.read_mail_templates(
        sheets_api.read_sheet(open_by_key=const.OPEN_BY_KEY, sheet_num=1, cell_range='A2:C')
    )
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
