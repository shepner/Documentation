import os

from app import app
from app import db
from models import FTSNote
from models import Note
from models import Task
from api import api
import views

api.setup()

if __name__ == '__main__':
    db.create_tables([FTSNote, Note, Task])
    app.run(debug=bool(os.environ.get('DEBUG')), host='0.0.0.0')