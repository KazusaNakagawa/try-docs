import os
import pickle
import sys

from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename

from src.google_api.config.log_conf import LogConf

TOKEN_JSON = 'token/token.json'


class ClientService(object):

    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/gmail.send']
        self.drive_scope = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        self.token_pickle = 'token/token.pickle'
        self.credentials = 'token/credentials.json'
        self.logger = LogConf().get_logger(logger=__file__)

    def get_service_gmail_v1(self):
        """ Gmail API 使用設定

        :return:
          Gmail v1 service
        """
        self.logger.info({
            'msd': 'アクセストークンの取得開始',
            'func': sys._getframe().f_code.co_name,
        })
        creds = None
        try:
            if os.path.exists(self.token_pickle):
                with open(self.token_pickle, 'rb') as token:
                    creds = pickle.load(token)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials, self.scope)
                    creds = flow.run_local_server()
                with open(self.token_pickle, 'wb') as token:
                    pickle.dump(creds, token)

            service = build('gmail', 'v1', credentials=creds)
            self.logger.info({
                'msd': 'アクセストークンの取得完了',
                'func': sys._getframe().f_code.co_name,
            })
            return service

        except Exception as ex:
            self.logger.info({
                'msd': 'アクセストークンの取得失敗',
                'func': sys._getframe().f_code.co_name,
                'ex': ex,
            })

    def get_service_drive_v3(self):
        """ Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.

        :return:
        """
        self.logger.info({
            'msd': 'アクセストークンの取得開始',
            'func': sys._getframe().f_code.co_name,
        })
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
            if os.path.exists(TOKEN_JSON):
                creds = Credentials.from_authorized_user_file(TOKEN_JSON, self.drive_scope)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials, self.drive_scope)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN_JSON, 'w') as token:
                    token.write(creds.to_json())

            service = build('drive', 'v3', credentials=creds)
            self.logger.info({
                'msd': 'アクセストークンの取得完了',
                'func': sys._getframe().f_code.co_name,
            })

            return service

        except Exception as ex:
            self.logger.error({
                'msd': 'アクセストークンの取得失敗',
                'func': sys._getframe().f_code.co_name,
                'ex': ex,
            })
            raise
