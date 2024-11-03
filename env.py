from dotenv import load_dotenv

import os

load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASS = os.environ.get("DB_PASS")
DB_ADRESS = os.environ.get("DB_ADRESS")
DB_NAME = os.environ.get("DB_NAME")
