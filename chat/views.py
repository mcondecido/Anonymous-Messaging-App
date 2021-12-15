# resource : https://www.youtube.com/watch?v=IpAk1Eu52GU&t=2297s
from django.shortcuts import get_object_or_404, render, redirect
from chat.models import Room, Message, PrivateRoom
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import generic
from chat.forms import PublicForm, PrivateForm
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    return render(request, 'home.html')

def public(request):
    return render(request, 'public.html')

def private(request):#, #generic.ListView):

    if request.method == "POST":
        form = PrivateForm(request.POST)

        if form.is_valid():
            room_details = form.save(commit=False)
            room_name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')

            #return HttpResponse(room_details)
            if PrivateRoom.objects.filter(name = room_name).exists():
                priv_room = PrivateRoom.objects.get(name=room_name)
                if check_password(password, priv_room.password):
                    request.session['form-submitted'] = room_name
                    return redirect("/priv_room/"+room_name+"/?username="+username)
                else:
                    messages.error(request,'password is not correct')
            else:
                password = make_password(password)
                new_room = PrivateRoom.objects.create(name=room_name, password=password)
                new_room.save()
                request.session['form-submitted'] = room_name
                return redirect("/priv_room/"+room_name+"/?username="+username)

    form = PrivateForm()
    private_room_list = PrivateRoom.objects.all()
    return render(request, 'private.html', {'form': form, 'private_room_list': private_room_list})

    """ model = PrivateRoom
    template_name = 'private.html'
    context_object_name = 'private_room_list' """
    """ def get_queryset(self):
        return PrivateRoom.objects.all() """


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
            return redirect('home')
    except PrivateRoom.DoesNotExist:
        return redirect('home')

    


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
    expiration_date = datetime.now() + timedelta(seconds=5)
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
    expiration_date = datetime.now() + timedelta(seconds=5)
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
