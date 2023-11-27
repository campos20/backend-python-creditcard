import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ADDRESS = os.environ["DB_ADDRESS"]
DB_NAME = os.environ["DB_NAME"]
DB_PORT = os.environ["DB_PORT"]
