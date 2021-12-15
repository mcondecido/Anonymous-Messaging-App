# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('public', views.public, name='public'),
    path('private', views.private, name='private'),
    path('<str:room>/', views.room, name='room'),
    path('<str:room>/', views.private_room, name='private_room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('send_email', views.send_email, name='send_email')
]