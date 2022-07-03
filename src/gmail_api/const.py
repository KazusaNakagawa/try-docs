import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SENDER_ADDRESS = os.environ.get("SENDER_ADDRESS")
TO_ADDRESS = os.environ.get("TO_ADDRESS")
