# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.shortcuts import get_object_or_404, render, redirect
from chat.models import Room, Message, PrivateRoom
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.views import generic
from chat.forms import PublicForm, PrivateForm
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

#def public(request):
#    return render(request, 'public.html')

def private(request):#, #generic.ListView):

    if request.method == "POST":
        form = PrivateForm(request.POST)

        if form.is_valid():
            room_details = form.save(commit=False)
            room_name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')

            if PrivateRoom.objects.filter(name = room_name).exists():
                priv_room = PrivateRoom.objects.get(name=room_name)
                if check_password(password, priv_room.password):
                    request.session['form-submitted'] = room_name
                    return redirect("/priv_room/"+room_name+"/?username="+username)
                else:
                    messages.error(request,'Password is incorrect. Try Again.')
                    return redirect('private')
            else:
                password = make_password(password)
                new_room = PrivateRoom.objects.create(name=room_name, password=password)
                new_room.save()
                request.session['form-submitted'] = room_name
                return redirect("/priv_room/"+room_name+"/?username="+username)

    form = PrivateForm()
    private_room_list = PrivateRoom.objects.all()
    return render(request, 'private.html', {'form': form, 'private_room_list': private_room_list})

def public(request):
    if request.method == "POST":
        form = PublicForm(request.POST)

        if form.is_valid():
            room_details = form.save(commit=False)
            room_name = form.cleaned_data.get('name')
            username = form.cleaned_data.get('username')

            if Room.objects.filter(name = room_name).exists():
                pub_room = Room.objects.get(name=room_name)
                return redirect("/pub_room/"+room_name+"/?username="+username)
            else:
                new_room = Room.objects.create(name=room_name)
                new_room.save()
                return redirect("/pub_room/"+room_name+"/?username="+username)
    
    form = PublicForm()
    public_room_list = Room.objects.all()
    return render(request, 'public.html', {'form': form, 'public_room_list': public_room_list})


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name = room)
    return render(request, 'room.html', {'username': username, 
    'room': room, 
    'room_details': room_details
    })

def private_room(request, room):
    username = request.GET.get('username')
    try:
        room_details = PrivateRoom.objects.get(name = room)
        if (request.session['form-submitted'] == room):   
            return render(request, 'privateroom.html', {'username': username, 
                'room': room, 
                'room_details': room_details
                })
        else:
            messages.error(request, "You can't access that room without logging in first.")
            return redirect('private')
    except PrivateRoom.DoesNotExist:
            messages.error(request, "The room you tried to access doesn't exist.")
            return redirect('private')



#checks if room already exists, makes one if doesnt, redirects if does
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name = room).exists():
        return redirect("/pub_room/"+room+"/?username="+username)
    else:
        new_room = Room.objects.create(name = room)
        new_room.save()
        return redirect("/pub_room/"+room+"/?username="+username)

#creates new message on submit
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    current_time = timezone.localtime(timezone.now())
    date_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
    #change timedelta(seconds=5) to (days=1) if you want 24 hour expiration
    expiration_date = datetime.now() + timedelta(days=1)
    new_message = Message.objects.create(text=message, user=username, room=room_id, expiration=expiration_date, date=date_time, private=False)
    new_message.save()
    return HttpResponse('Message sent')

def privatesend(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    current_time = timezone.localtime(timezone.now())
    date_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
    #change timedelta(seconds=5) to (days=1) if you want 24 hour expiration
    expiration_date = datetime.now() + timedelta(days=1)
    new_message = Message.objects.create(text=message, user=username, room=room_id, private=True, expiration=expiration_date, date=date_time)
    new_message.save()
    return HttpResponse('Message sent')

#displays all messages in room
def getMessages(request, room):
    now = datetime.now()
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id, private=False, expiration__gt=now)
    return JsonResponse({'messages': list(messages.values())})

def getPrivateMessages(request, room):
    now = datetime.now()
    room_details = PrivateRoom.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id, private=True, expiration__gt=now)
    return JsonResponse({'messages': list(messages.values())})
