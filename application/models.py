from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Thread(models.Model):
    """

    """
    participants = models.JSONField(null=True)
    created = models.DateTimeField(null=False, default=timezone.now)
    updated = models.DateTimeField(null=False)


class Message(models.Model):
    """

    """
    sender = models.ForeignKey(User, null=False, related_name='user', on_delete=models.SET('User was delete'))
    text = models.TextField(null=False)
    thread = models.ForeignKey(Thread, null=False, related_name='thread', on_delete=models.CASCADE)
    created = models.DateTimeField(null=False, default=timezone.now)
    is_read = models.BooleanField(null=False, default=False)
