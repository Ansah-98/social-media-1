from multiprocessing import context
from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import  Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except :
            messages.error(request,'user is not found')
        user = authenticate(request, username = username, password=password)  

        if user is not None:
            login(request,user) 
            return redirect('home')
        else:
            messages.error(request,'wrong credentials')
    
    context= {'obj':'obj'}
    return render(request,'socials/login_register.html', context )

def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        c_password = request.POST['c-password']
        email= request.POST['email']

        if c_password != password :
            messages.error(request,'confirmed password not the same password')
        user = User.objects.filter(username= username).first() or User.objects.filter(email= email).first()

        if user is not None:
            messages.error(request,f'{user.username} already exist')
        
        else:
            user = User.objects.create_user(username= username,password =password,email =email)
            user.save()
            login(request,user)
            return redirect('home')
    return render(request,'socials/login_register.html')
def signOut(request):
    

    logout(request)
    return redirect('login')
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
    room_messages = room.message_set.all()
    if request.method == 'POST':
        comment = request.POST['comment']
        new_comment= Message.objects.create(user=request.user, room = room, body=comment)
        new_comment.save()
        return redirect('room', pk = room.id)


    context = {'room':room,'room_messages':room_messages}
    return render(request,'socials/room.html',context)

@login_required(login_url='login')
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