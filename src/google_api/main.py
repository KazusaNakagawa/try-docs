import const

from gmail_api import GmailApi
from drive_api import DriveApi


def main_attach_file():
    """ 添付ファイルつき Gmail送信 """
    gmail_api = GmailApi(sender=const.SENDER_ADDRESS, to=const.TO_ADDRESS)

    # メール本文の作成
    subject = 'メール送信自動化テスト_ Class Gmail API'
    message_text = 'メール送信の自動化テストをしています。 zip 添付'
    message = gmail_api.create_message_attach_file(subject=subject, message_text=message_text)

    gmail_api.send_message(user_id='me', msg=message)


def main():
    """ テキスト文のみ Gmail 送信 """
    gmail_api = GmailApi(sender=const.SENDER_ADDRESS, to=const.TO_ADDRESS)

    # メール本文の作成
    subject = 'メール送信自動化テスト_ Class Gmail API'
    message_text = 'メール送信の自動化テストをしています。'
    message = gmail_api.create_message(subject_=subject, msg_text=message_text)

    gmail_api.send_message(user_id='me', msg=message)


def read_drive_files():
    drive_api = DriveApi()
    # drive_api.service_files()
    drive_api.read_spreadsheet()


if __name__ == '__main__':
    # main_attach_file()
    # main()
    read_drive_files()
