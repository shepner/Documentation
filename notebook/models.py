import datetime
import re

from flask import Markup
from huey import crontab
from markdown import markdown
from micawber import parse_html
from peewee import *
from playhouse.sqlite_ext import FTSModel

from app import db, huey, oembed

def rich_content(content, maxwidth=300):
    html = parse_html(
        markdown(content),
        oembed,
        maxwidth=maxwidth,
        urlize_all=True)
    return Markup(html)

class Note(Model):
    STATUS_VISIBLE = 1
    STATUS_ARCHIVED = 2
    STATUS_DELETED = 9

    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=STATUS_VISIBLE, index=True)
    reminder = DateTimeField(null=True)
    reminder_sent = BooleanField(default=False)

    class Meta:
        database = db

    def html(self):
        return rich_content(self.content)

    def is_finished(self):
        if self.tasks.exists():
            return not self.tasks.where(Task.finished == False).exists()

    def get_tasks(self):
        return self.tasks.order_by(Task.order)

    def parse_content_tasks(self):
        # Split the list of tasks from the surrounding content, returning both.
        content = []
        tasks = []
        for line in self.content.splitlines():
            if line.startswith('@!'):
                tasks.append((True, line[2:].strip()))
            elif line.startswith('@'):
                tasks.append((False, line[1:].strip()))
            else:
                content.append(line)
        return '\n'.join(content), tasks

    def unparse_content(self):
        content = [self.content]
        for task in self.get_tasks():
            content.append('%s %s' % ('@!' if task.finished else '@',
                                      task.title))
        return '\n'.join(line for line in content if line)

    def save(self, *args, **kwargs):
        # Split out the text content and any tasks.
        self.content, tasks = self.parse_content_tasks()

        # Update the timestamp.
        self.timestamp = datetime.datetime.now()

        # Save the note.
        with db.atomic():
            ret = super(Note, self).save(*args, **kwargs)

            # Store the tasks in the database.
            if tasks:
                Task.delete().where(Task.note == self).execute()
                for idx, (finished, title) in enumerate(tasks):
                    Task.create(
                        note=self,
                        finished=finished,
                        title=title,
                        order=idx)

            # Store the content for full-text search.
            FTSNote.store_note(self)

        return ret

    @classmethod
    def public(cls):
        return (Note
                .select()
                .where(Note.status == Note.STATUS_VISIBLE)
                .order_by(Note.timestamp.desc()))

    @classmethod
    def search(cls, search_term, days_to_search=None):
        words = [word.strip() for word in search_term.split() if word]
        if not words:
            return Note.select().where(Note.id == 0)
        else:
            search = ' '.join(words)

        query = (Note
                 .select(Note, FTSNote.rank().alias('score'))
                 .join(FTSNote, on=(Note.id == FTSNote.docid))
                 .where(
                     (Note.status == Note.STATUS_VISIBLE) &
                     (FTSNote.match(search)))
                 .order_by(FTSNote.rank()))

        if days_to_search:
            today = datetime.date.today()
            query = query.where(
                Note.timestamp.between(
                    today - datetime.timedelta(days=int(days_to_search)),
                    datetime.datetime.now()))

        return query


class FTSNote(FTSModel):
    HTML_RE = re.compile('<.+?>')
    content = TextField()

    class Meta:
        database = db
        
    @staticmethod
    def get_search_content(note):
        content = [FTSNote.HTML_RE.sub('', note.html())]
        for task in note.get_tasks():
            content.append(FTSNote.HTML_RE.sub('', task.html()))
        return '\n'.join(line for line in content if line)

    @classmethod
    def store_note(cls, note):
        content = FTSNote.get_search_content(note)
        try:
            FTSNote.get(FTSNote.docid == note.id)
        except FTSNote.DoesNotExist:
            FTSNote.create(docid=note.id, content=content)
        else:
            (FTSNote
             .update(content=content)
             .where(FTSNote.docid == note.id)
             .execute())

    


class Task(Model):
    note = ForeignKeyField(Note, related_name='tasks')
    title = CharField(max_length=255)
    order = IntegerField(default=0)
    finished = BooleanField(default=False)

    class Meta:
        database = db

    def html(self):
        return rich_content(self.title)


@huey.periodic_task(crontab(minute='*/5'))
def send_note_reminders():
    query = (Note
             .select()
             .where(
                 (Note.status != Note.STATUS_DELETED) &
                 Note.reminder.is_null(False) &
                 (Note.reminder < datetime.datetime.now()) &
                 (Note.reminder_sent == False))
             .order_by(Note.reminder))

    for note in query:
        app.logger.info(
            'Sending reminder for Note(%s), reminder timestamp = %s.' %
            (note.id, note.reminder.strftime('%Y-%m-%d %H:%M')))

        try:
            mailer.send(
                to=app.config['REMINDER_EMAIL'],
                subj='[notes] reminder',
                body=note.content)
        except:
            app.logger.info('Sending reminder failed for Note(%s).' % note.id)
        else:
            app.logger.info('Reminder for Note(%s) sent successfully.' %
                            note.id)
            Note.update(reminder_sent=True).where(Note.id == note.id).execute()