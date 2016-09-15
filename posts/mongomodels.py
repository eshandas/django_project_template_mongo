from mongoengine import Document
from mongoengine import fields


class Post(Document):
    title = fields.StringField(required=True, max_length=50, unique=True)
    body = fields.StringField(required=True)

    def __unicode__(self):
        return self.title
