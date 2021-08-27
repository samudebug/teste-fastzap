from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    participants = models.ManyToManyField(User)


class Message(models.Model):
    text_content = models.CharField(max_length=500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", default=None)
    timestamp = models.DateTimeField()
    