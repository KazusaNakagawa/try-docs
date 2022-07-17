import base64
import pickle
import os.path

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

# If modifying these scopes, delete the file token.json.

TOKEN_JSON = 'token/token.json'


class ClientService(object):
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/gmail.send']
        self.drive_scope = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    def get_service_gmail_v1(self):
        """ アクセストークンの取得

        :return:
          Gmail v1 service
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

    def get_service_drive_v3(self):
        """ Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.

        :return:
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_JSON):
            creds = Credentials.from_authorized_user_file(TOKEN_JSON, self.drive_scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'token/credentials.json', self.drive_scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_JSON, 'w') as token:
                token.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)
