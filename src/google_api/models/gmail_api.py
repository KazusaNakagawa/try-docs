import base64

from apiclient import errors
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename

from src.google_api.models.client_service import ClientService


class GmailApi(ClientService):

    def __init__(self, sender, to, zip_dir=None, zip_name=None):

        """ gmail operations with the Gmail API

        :param
          sender(str): Sender Address
          to(str): To Address
          zip_dir(str): 添付対象 zip Directory Name
          zip_name(str): 添付対象 zip Name
        """
        super().__init__()
        self.sender = sender
        self.to = to
        self.zip_dir = zip_dir
        self.zip_name = zip_name
        self.service = self.get_service_gmail_v1()

    def create_message(self, subject_, msg_text):
        """ メール本文の作成 """

        msg = MIMEText(msg_text)
        msg['to'] = self.to
        msg['from'] = self.sender
        msg['subject'] = subject_
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())

        return {'raw': encode_message.decode()}

    def create_message_attach_file(self, subject, message_text):
        """ メール本文の作成 添付ファイルつき """

        msg = self._attach_file()

        msg['to'] = self.to
        msg['from'] = self.sender
        msg['subject'] = subject

        # ファイルを添付
        msg.attach(MIMEText(message_text))
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())

        return {'raw': encode_message.decode()}

    def _attach_file(self):
        """ ファイルを添付

        :param
          attach_file_path(str): 添付対象ファイル path

        :return
          msg(class: email.mime.multipart.MIMEMultipart)
        """
        attach_file_path = f'{self.zip_dir}/{self.zip_name}'

        msg = MIMEMultipart()
        with open(attach_file_path, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(attach_file_path)
            )
        part['Content-Disposition'] = f"attachment; filename={basename(attach_file_path)}"
        msg.attach(part)

        return msg

    def send_message(self, user_id, msg):
        """ メール送信の実行 """
        try:
            msg = (self.service.users().messages().send(userId=user_id, body=msg)
                   .execute())
            print(f"Message Id: {msg['id']}")

            return msg
        except errors.HttpError as error:
            print(f"An error occurred: {error}")

    def auto_reply(self):
        """ 受付完了自動返信メール

        - クライアントから受信
        - 受付検知
        - 本関数呼び出し
        - 受付完了メールの送信

        :return:
        """
