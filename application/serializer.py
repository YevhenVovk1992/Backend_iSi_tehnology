from django.contrib.auth.models import User
from rest_framework import serializers

from application import models


class ThreadSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        instance = models.Thread.objects.get_or_create(
            participants=validated_data['participants']
        )
        return instance[0]

    class Meta:
        model = models.Thread
        fields = ('id', 'participants', 'created', 'updated')


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='pk')
    thread = serializers.SlugRelatedField(queryset=models.Thread.objects.all(), slug_field='pk')

    class Meta:
        model = models.Thread
        fields = ('__all__', )