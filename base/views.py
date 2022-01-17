from django.http import HttpResponse
from os import name
from .models import Room, Topic
from django.shortcuts import render, redirect
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid:
            form.save()
            user = User.objects.get(username = request.POST.get('username'))
            print(user)
            login(request, user)
            return redirect('home')
    form = UserForm()
    action = "register"
    context = {"action": action, "form": form}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    #user = request.user
    logout(request)
    messages.success(request, "User Logged out")
    return redirect('home')

def loginPage(request):

    if request.user.is_authenticated :
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User not exists!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "User Logged-in")
            return redirect('home')
        else:
            messages.error(request, "Username and Password not matched ")
    action="login"
    context = {"action": action}
    return render(request, 'base/login_register.html', context)

def home(request,):
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

@login_required
def add_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url= '/login')
def edit_room(request, pk):
    
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not authorized to perform this action !")
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            room = form.save(commit=False)
            room.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not authorized to perform this action !")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {"obj": room}

    return render(request, 'base/delete_form.html', context)
