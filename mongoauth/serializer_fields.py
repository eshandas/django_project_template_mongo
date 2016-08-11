from rest_framework import serializers
from bson.objectid import ObjectId


class ObjectIdField(serializers.CharField):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        return ObjectId(data)
