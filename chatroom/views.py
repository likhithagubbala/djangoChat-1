from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message

@login_required
def HomeView(request):
    if request.method == "POST":
        username = request.POST["username"]
        room = request.POST["room"]
        try:
            existing_room = Room.objects.get(room_name__iexact=room)
        except Room.DoesNotExist:
            existing_room = Room.objects.create(room_name=room)
        return redirect("room", room_name=existing_room.room_name, username=username)

    all_rooms = Room.objects.all()
    context = {
        'rooms': all_rooms
    }
    return render(request, 'home.html', context)

@login_required
def RoomView(request, room_name, username):
    try:
        existing_room = Room.objects.get(room_name__iexact=room_name)
    except Room.DoesNotExist:
        return redirect('home')

    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": existing_room.room_name
    }
    return render(request, 'room.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
