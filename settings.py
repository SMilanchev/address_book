import os

import dotenv

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv()

AB_HOST = os.environ["AB_HOST"]
AB_PORT = int(os.environ['AB_PORT'])
DB_NAME = 'address_db'
