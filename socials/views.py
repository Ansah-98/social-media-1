from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import  Q
# Create your views here.
def home(request):
    
    
    q = request.GET.get('q')
    if q is None:
        topic = Topic.objects.all()
        rooms = Room.objects.all()
    else:
        topic = Topic.objects.filter(title__icontains = q)
        
        rooms = Room.objects.filter(Q(topic__title__icontains =q)|
        Q(description__icontains =q)|
        Q(name__icontains=q)|
        Q(host__username__icontains=q))
    

    room_count = rooms.count()
    context={'rooms':rooms, 'topics': topic, 'room_count':room_count}
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
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request,'socials/room_form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    if request.method =='P0ST':
        room.delete()
        return redirect('home')
    
    return render(request, 'socials/delete.html',{'obj':room.name})