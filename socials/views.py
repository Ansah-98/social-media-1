from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm
# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context={'rooms':rooms}
    return render(request,'socials/index.html',context)
def room(request,pk):

    room = Room.objects.get(id = pk)
    context = {'room':room}
    return render(request,'socials/room.html',context)

def createroom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'socials/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance =room)
    context = {'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST, instance= room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request,'socials/room_form.html', context)