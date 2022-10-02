import os

import env

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs('db_task', exist_ok=True)

MONGO_URL = os.environ.get("MONGO_URL")
URL_MSG_SEND = os.environ.get("URL_MSG_SEND")
URL_SCHEDULER = 'sqlite:///'+ os.path.join(basedir, 'db_task', 'jobs.sqlite')
TOKEN = os.environ.get("TOKEN")