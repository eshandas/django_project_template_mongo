from rest_framework_mongoengine.serializers import (
    DocumentSerializer,
)
from rest_framework import serializers

from .mongomodels import (
    Post,
)


class PostSerializer(DocumentSerializer):
    isActive = serializers.BooleanField(
        source='is_active')

    class Meta:
        model = Post
        fields = '__all__'
