from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Message

def HomeView(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        room = request.POST.get("room", "").strip()

        if not username:
            messages.error(request, "Username cannot be empty.")
            return redirect('home')

        if not room:
            messages.error(request, "Room name cannot be empty.")
            return redirect('home')

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

def RoomView(request, room_name, username):
    if not username:
        return redirect('home')

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

@login_required
def SendMessageView(request, room_name):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        username = request.user.username  # Ensure the user is authenticated

        try:
            room = Room.objects.get(room_name__iexact=room_name)
        except Room.DoesNotExist:
            return redirect('home')

        if message_content:
            Message.objects.create(room=room, author=username, content=message_content)
        
        return redirect('room', room_name=room_name, username=username)
    else:
        return redirect('home')  # Redirect to home if someone tries to access via GET

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def SignupView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'signup.html')
