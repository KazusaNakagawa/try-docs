import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Gmail
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')
TO_ADDRESS = os.environ.get('TO_ADDRESS')

# PySimpleGUI
PY_SIMPLE_GUI = {
 'font': '14',
 'theme': 'BlueMono',
}

# SpreadSheet
ACCOUNT_SHEET_NAME = ['ID', 'アカウント名', 'メールアドレス To', 'zip パスワード']
MAIL_TEMPLATE = ['ID', '件名', '本文']
OPEN_BY_KEY = os.environ.get('OPEN_BY_KEY')

# Zip
ZIP_DIR = 'zip_storage'
ZIP_NAME = 'sample.zip'

# Token Key
CREDENTIALS = 'token/credentials.json'
SECRET_CREDENTIALS_JSON_OATH = 'token/gmail-api-355022-service-account-key.json'
TOKEN_JSON = 'token/token.json'
TOKEN_PICKLE = 'token/token.pickle'
