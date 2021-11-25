# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.db import models
from datetime import datetime

# create room and message classes
class Room(models.Model):
    name = models.CharField(max_length=100)
class Message(models.Model):
    text = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)