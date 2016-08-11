from mongoengine import Document
from mongoengine import fields

import datetime


class User(Document):
    email = fields.StringField(required=True, max_length=50, unique=True)
    password = fields.StringField(required=True)
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)
    mobile = fields.StringField(max_length=15)
    address_line_1 = fields.StringField()
    address_line_2 = fields.StringField()
    city = fields.StringField()
    state = fields.StringField()
    zip = fields.StringField()
    created_by = fields.ObjectIdField()
    created_on = fields.DateTimeField()
    last_updated_by = fields.ObjectIdField()
    last_updated_on = fields.DateTimeField()
    is_active = fields.BooleanField()
    is_email_verified = fields.BooleanField(default=False)
    is_mobile_verified = fields.BooleanField(default=False)
    last_login = fields.DateTimeField()

    meta = {'indexes': [
        {'fields': ['$email', "$first_name", "$last_name"],
         'default_language': 'english',
         'weights': {'email': 10, 'first_name': 5, 'last_name': 5}}
    ]}

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.datetime.now()
        self.last_updated_on = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.first_name
