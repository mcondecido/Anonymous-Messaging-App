# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.contrib import admin
from .models import Room, PrivateRoom, Message

# making admin views
admin.site.register(Room)
admin.site.register(PrivateRoom)
admin.site.register(Message)