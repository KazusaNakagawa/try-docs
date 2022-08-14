import base64
import re

from apiclient import errors
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename

from models.client_service import ClientService
from config.log_conf import LogConf


class GmailApi(ClientService):

    def __init__(self, sender=None, to=None):

        """ gmail operations with the Gmail API

        :param
          sender(str): Sender Address
          to(str): To Address
        """
        super().__init__()
        self.sender = sender
        self.to = to
        self.service = self.get_service_gmail_v1()
        self.logger = LogConf().get_logger(__file__)

    def create_message(self, subject_, msg_text):
        """ メール本文の作成 """

        msg = MIMEText(msg_text)
        msg['to'] = self.to
        msg['from'] = self.sender
        msg['subject'] = subject_
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())

        return {'raw': encode_message.decode()}

    def create_message_attach_file(self, attach_files, subject, message_text):
        """ メール本文の作成 添付ファイルつき """

        msg = self._attach_file(attach_files)

        msg['to'] = self.to
        msg['from'] = self.sender
        msg['subject'] = subject

        # ファイルを添付
        msg.attach(MIMEText(message_text))
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())

        return {'raw': encode_message.decode()}

    @classmethod
    def _attach_file(cls, attach_files):
        """ ファイルを添付

        :param
          attach_file_path(str): 添付対象ファイル path

        :return
          msg(class: email.mime.multipart.MIMEMultipart)
        """
        msg = MIMEMultipart()

        for attach_file in attach_files:
            with open(attach_file, "rb") as f:
                part = MIMEApplication(
                    f.read(),
                    Name=basename(attach_file)
                )
            part['Content-Disposition'] = f"attachment; filename={basename(attach_file)}"
            msg.attach(part)

        return msg

    def send_message(self, user_id, msg):
        """ メール送信の実行 """
        try:
            msg = self.service.users().messages().send(userId=user_id, body=msg).execute()
            self.logger.info({
                'Message Id': msg['id'],
                'msg': 'OK Send mail',
            })

        except errors.HttpError as error:
            self.logger.error({
                'Message Id': msg['id'],
                'error': error,
            })

    def auto_reply(self):
        """ 受付完了自動返信メール

        - クライアントから受信
        - 受付検知
        - 本関数呼び出し
        - 受付完了メールの送信

        :return:
        """

    def receive_gmail(self, max_results=10, query=None) -> list or bool:
        """Gmail 一覧を取得

        """
        # メッセージの一覧を取得
        messages = self.service.users().messages()
        msg_list = messages.list(userId='me', maxResults=max_results, q=query).execute()

        if msg_list['resultSizeEstimate'] == 0:
            return False

        receives = []

        # 取得したメッセージの一覧を表示
        if msg_list['resultSizeEstimate'] == 201:
            for msg in msg_list['messages']:
                topid = msg['id']
                msg = messages.get(userId='me', id=topid).execute()

                # 受信時間を抽出 ex: Sat, 13 Aug 2022 02:04:12 -0700 (PDT)
                received = msg['payload']['headers'][1]['value']
                match = re.search(r'[a-zA-Z]{3}, \d{2} [a-zA-Z]{3} \d{4} (\d{2}:\d{2}:\d{2}) -\d{4} \(PDT\)$', received)
                if match:
                    received = match.group()

                # TODO: sender, title, subject
                data = {
                    'Received': received,
                    'Delivered-To': msg['payload']['headers'][0]['value'],
                    'snippet': msg['snippet'],
                }
                receives.append(data)

        return receives

    def receive_gmail_threads(self):
        """Gmail 一覧を取得

        """
        # メッセージの一覧を取得
        messages = self.service.users().threads()
        msg_list = messages.list(userId='me', maxResults=5).execute()

        # 取得したメッセージの一覧を表示
        for msg in msg_list['threads']:
            topid = msg['id']
            msg = messages.get(userId='me', id=topid).execute()
            print("---")
            print(msg['messages'][0]['snippet'])
