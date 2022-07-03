import base64
import pickle
import os.path

from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import const


class GmailApi(object):

    def __init__(self, sender, to):
        """ gmail operations with the Gmail API

        :param
          sender(str): Sender Address
          to(str): To Address
        """
        self.scope = ['https://www.googleapis.com/auth/gmail.send']
        self.sender = sender
        self.to = to
        self.service = self.get_access_token()

    def get_access_token(self):
        """ アクセストークンの取得

        :return:
          service
        """
        creds = None
        if os.path.exists('token/token.pickle'):
            with open('token/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'token/credentials.json', self.scope)
                creds = flow.run_local_server()
            with open('token/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def create_message(self, subject_, msg_text):
        """ メール本文の作成 """

        msg = MIMEText(msg_text)
        msg['to'] = self.to
        msg['from'] = self.sender
        msg['subject'] = subject_
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())

        return {'raw': encode_message.decode()}

    def send_message(self, user_id, msg):
        """ メール送信の実行 """
        try:
            msg = (self.service.users().messages().send(userId=user_id, body=msg)
                   .execute())
            print(f"Message Id: {msg['id']}")

            return msg
        except errors.HttpError as error:
            print(f"An error occurred: {error}")


if __name__ == '__main__':
    gmail_api = GmailApi(sender=const.SENDER_ADDRESS, to=const.TO_ADDRESS)

    # メール本文の作成
    subject = 'メール送信自動化テスト_ Class Gmail API'
    message_text = 'メール送信の自動化テストをしています。'
    message = gmail_api.create_message(subject_=subject, msg_text=message_text)

    gmail_api.send_message(user_id='me', msg=message)
