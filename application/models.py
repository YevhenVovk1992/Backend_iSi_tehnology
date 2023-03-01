from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Thread(models.Model):
    """

    """
    participants = models.JSONField(null=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)


class Message(models.Model):
    """

    """
    sender = models.ForeignKey(User, null=False, related_name='user', on_delete=models.SET('User was delete'))
    text = models.TextField(null=True)
    thread = models.ForeignKey(Thread, null=False, related_name='thread', on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    is_read = models.BooleanField(null=False, default=False)
