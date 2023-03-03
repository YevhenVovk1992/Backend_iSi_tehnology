from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Thread(models.Model):
    """
    The model that describes Thread object
    """
    participants = models.JSONField(null=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)


class Message(models.Model):
    """
    The model that describes Message object.
    """
    sender = models.ForeignKey(User, null=False, related_name='user_messages', on_delete=models.SET('User was delete'))
    text = models.TextField(null=True)
    thread = models.ForeignKey(Thread, null=False, related_name='thread_messages', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    is_read = models.BooleanField(null=False, default=False)
