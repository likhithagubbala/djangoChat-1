from django.shortcuts import render, redirect
from .models import Room, Message

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