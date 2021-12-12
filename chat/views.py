# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.shortcuts import render, redirect
from chat.models import Room, PrivateRoom, Message
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.views import generic
from django.contrib.auth.hashers import check_password
from django.views.generic.base import TemplateView
import json


# Create your views here.
#def home(request):
#    return render(request, 'home.html')
class HomeView(generic.ListView):
    model = Room
    template_name = 'home.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        return Room.objects.all()

class RoomCreateView(TemplateView): 
    template_name = 'room_create.html'

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name = room)
    return render(request, 'room.html', {'username': username, 
    'room': room, 
    'room_details': room_details
    })

#checks if room already exists, makes one if doesnt, redirects if does
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    password = request.POST['password']
    private = bool(request.POST['private'])

    return HttpResponse(private)

    if Room.objects.filter(name = room).exists():
        if private:
            curr_pass = PrivateRoom.objects.filter(name = room).only("password") #not sure if this is the right way to access password field
            pass_match = check_password(curr_pass, password)
            if pass_match:
                return redirect("/"+room+"/?username="+username)
            else:
                return HttpResponse("Incorrect Password.")
        return redirect("/"+room+"/?username="+username)
    else:
        return HttpResponse("Room with entered name does not exist.")

def makeroom(request):
    room = request.POST['room_name']
    username = request.POST['username']
    password = request.POST['password']
    private = bool(request.POST['private'])

    if Room.objects.filter(name = room).exists():
        return HttpResponse('Room with entered name already exists. Please choose a different room name.')
    else:
        if private:
            new_room = Room.objects.create(name = room, private=True)
            priv_room = PrivateRoom.objects.create(name = room, private=True, password=password)
            priv_room.save()
        else:
            new_room = Room.objects.create(name = room)
        print(private)
        new_room.save()

        return redirect("/"+room+"/?username="+username)

#creates new message on submit
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(text=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent')

#displays all messages in room
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id, private=False)
    return JsonResponse({'messages': list(messages.values())})


def send_email(request):
    try:
        recipient= request.POST['recipient']
        room_name = request.POST['room_name']
        msg = EmailMessage('Join this anonymous group chat session!',
                        ' Go to this link - https://anonymous-chat-app-4501.herokuapp.com/ \n Create a new username and enter this room code: ' + room_name + '.', to=[recipient])
        msg.send()
        return HttpResponse('Email sent!')
    except:
        return HttpResponse('Incorrect email format!')
