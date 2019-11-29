from flask import render_template
from flask import request
from flask_peewee.rest import Authentication
from flask_peewee.rest import RestAPI
from flask_peewee.rest import RestResource
from flask_peewee.utils import get_object_or_404

from app import app
from models import Note
from models import Task


# Allow GET and POST requests without requiring authentication.
auth = Authentication(protected_methods=['PUT', 'DELETE'])
api = RestAPI(app, default_auth=auth)

class NoteResource(RestResource):
    fields = ('id', 'content', 'timestamp', 'status')
    paginate_by = 30

    #def get_urls(self):
    #    urls = super(NoteResource, self).get_urls()
    #    return (
    #        ('/search/', self.search),
    #        ('/<pk>/details/', self.note_details),
    #    ) + urls
      
    def get_urls(self):
        return (
            ('/search/', self.search),
        ) + super(NoteResource, self).get_urls()

    #def search(self):
    #    query = request.args.get('query')
    #    notes = Note.search(
    #        request.args.get('query') or '',
    #        request.args.get('days'))
    #    notes = self.process_query(notes)
    #    return self.paginated_object_list(notes)
      
    def search(self):
        query = request.args.get('query')
        notes = Note.search(request.args.get('query') or '')
        notes = self.process_query(notes)  # Apply any filters, etc.
        return self.paginated_object_list(notes)

    def note_details(self, pk):
        note = get_object_or_404(self.get_query(), self.pk == pk)
        return self.response({
            'content': note.unparse_content(),
            'reminder': (note.reminder.strftime('%Y-%m-%dT%H:%M')
                         if note.reminder else None),
        })

    def get_query(self):
        return Note.public()

    def prepare_data(self, obj, data):
        data['rendered'] = render_template('note.html', note=obj)
        return data

class TaskResource(RestResource):
    paginate_by = 50

api.register(Note, NoteResource)
api.register(Task, TaskResource)