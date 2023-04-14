import os
from os.path import join, dirname
from dotenv import load_dotenv


def GET_KEY(key_name):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    KEY = os.environ.get(key_name)
    return KEY