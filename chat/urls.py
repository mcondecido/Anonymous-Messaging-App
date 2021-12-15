# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('public/', views.public, name='public'),
    path('private/', views.private, name='private'),
    path('pub_room/<str:room>/', views.room, name='room'),
    path('priv_room/<str:room>/', views.private_room, name='private_room'),
    path('public/checkview', views.checkview, name='checkview'),
    path('send/pub/', views.send, name='send'),
    path('send/priv/', views.privatesend, name='privatesend'),
    path('getMessages/pub/<str:room>/', views.getMessages, name='getMessages'),
    path('getMessages/priv/<str:room>/', views.getPrivateMessages, name='getPrivateMessages'),
    path('send_email/', views.send_email, name='send_email')
]