from playhouse.migrate import *

from app import db
from models import *


def run_migration():
    migrator = SqliteMigrator(db)
    with db.atomic():
        migrate(
            migrator.drop_column('note', 'reminder_task_created'),
        )
        FTSNote.create_table(True)

    with db.atomic():
        for note in Note.select():
            FTSNote.store_note(note)


if __name__ == '__main__':
    run_migration()