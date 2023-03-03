from django.contrib.auth.models import User
from rest_framework import serializers

from application import models


class MessageForThreadSerializer(serializers.ModelSerializer):
    """
    Serializer that receives messages for a Thread in ThreadWithMessagesSerializer
    """
    sender = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='pk')

    class Meta:
        model = models.Message
        fields = ('id', 'sender', 'text', 'created', 'is_read')


class ThreadWithMessagesSerializer(serializers.ModelSerializer):
    """
    A serializer that outputs data about Thread and
    all messages related with the Thread
    """
    created = serializers.DateTimeField(read_only=True)
    thread_messages = MessageForThreadSerializer(many=True, read_only=True)

    class Meta:
        model = models.Thread
        fields = ('id', 'participants', 'created', 'updated', 'thread_messages')


class ThreadSerializer(serializers.ModelSerializer):
    """
    A serializer that creates new Thread or
    outputs data about Thread if it has been created.
    """
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
    """
    Serializer for Message model
    """
    sender = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='pk')
    thread = serializers.SlugRelatedField(queryset=models.Thread.objects.all(), slug_field='pk')

    class Meta:
        model = models.Message
        fields = ('id', 'sender', 'text', 'thread', 'created', 'is_read')