import os
from os.path import join, dirname
from dotenv import load_dotenv


def DB_KEY ():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    DATABASE_PASSWORD = os.environ.get("MONGO_DB_KEY")

    return DATABASE_PASSWORD

def SOLSCAN_API_KEY(): 
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    API_KEY = os.environ.get("SOLSCAN_API_KEY")

    return API_KEY

def IGNORED_WALLETS(): 
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    ignored_wallets_array = os.environ.get("IGNORED_WALLETS")

    return ignored_wallets_array