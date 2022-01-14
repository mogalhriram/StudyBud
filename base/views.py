from os import name
from .models import Room, Topic
from django.shortcuts import render, redirect
from .forms import RoomForm
from django.db.models import Q

# Create your views here.


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)

    return render(request, 'base/login_register.html')

def home(request, **kwargs):
    query = request.GET.get('q')
    rooms = Room.objects.all()
    if query:
        topic = Topic.objects.distinct().filter(name__icontains = query)
        rooms = Room.objects.distinct().filter( Q(topic__in =topic)
         | Q(title__icontains=query)
         | Q(description__icontains=query)
         ) 
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context= context)

def add_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'base/room_form.html', context)


def edit_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            room = form.save(commit=False)
            room.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {"obj": room}

    return render(request, 'base/delete_form.html', context)
