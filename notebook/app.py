import os

from flask import Flask
from huey import RedisHuey
from micawber import bootstrap_basic
from playhouse.sqlite_ext import SqliteExtDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, 'notes.db')
DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

db = SqliteExtDatabase(app.config['DATABASE'], pragmas=[('journal_mode', 'wal')])
huey = RedisHuey()
oembed = bootstrap_basic()