# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')


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

    if Room.objects.filter(name = room).exists():
        return redirect("/"+room+"/?username="+username)
    else:
        new_room = Room.objects.create(name = room)
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
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({'messages': list(messages.values())})