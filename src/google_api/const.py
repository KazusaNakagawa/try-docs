import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Gmail
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')
TO_ADDRESS = os.environ.get('TO_ADDRESS')

# SpreadSheet
OPEN_BY_KEY = os.environ.get('OPEN_BY_KEY')
