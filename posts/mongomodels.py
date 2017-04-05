from mongoengine import DynamicDocument
from mongoengine import fields


class Post(DynamicDocument):
    title = fields.StringField(
        required=True,
        max_length=50,
        unique=True)
    body = fields.StringField(
        required=True)
    is_active = fields.BooleanField()

    def __unicode__(self):
        return self.title
