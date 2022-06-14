from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
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
    return render(request,'socials/login-register.html', context )

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
    return render(request,'socials/login-register.html')
def signOut(request):
    

    logout(request)
    return redirect('login')
def home(request):  

    q = request.GET.get('q')
    if q is None:
        topic = Topic.objects.all()
        rooms = Room.objects.all()
        room_messages = Message.objects.all()

    else:
        room_messages = Message.objects.filter(Q(room__topic__title__icontains=q)|
        Q(user__username__icontains=q))
        topic = Topic.objects.filter(title__icontains = q) 
        rooms = Room.objects.filter(Q(topic__title__icontains =q)|
        Q(description__icontains =q)|
        Q(name__icontains=q)|
        Q(host__username__icontains=q))

    
    room_count = rooms.count()
    context={'rooms':rooms, 'topics': topic[:5], 'room_count':room_count, 'message':room_messages , }
    return render(request,'socials/index.html',context)

def room(request,pk):

    room = Room.objects.get(id = pk)
    participant =room.participants.all()
    room_messages = room.message_set.all()
    if request.method == 'POST':
        comment = request.POST['comment']
        new_comment= Message.objects.create(user=request.user, room = room, body=comment)
        room.participants.add(request.user)
        new_comment.save()
        return redirect('room', pk = room.id)

    context = {'room':room,'room_messages':room_messages, 'participants':participant}
    return render(request,'socials/room.html',context)

@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST['topic']
        topic,created = Topic.objects.get_or_create(title = topic_name)
        Room.objects.create(
        host = request.user ,
        topic = topic,
        name = request.POST['name'],
        description = request.POST['description']
    )
        return redirect('home') 
    context = {'form':form,'topics':topics}
    return render(request,'socials/create-room.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics= Topic.objects.all()
    context = {'form':form,'topics':topics, 'room':room}
    if request.method == 'POST':
        topic_name = request.POST['topic']
        topic,created = Topic.objects.get_or_create(title = topic_name)
        room.name  = request.POST['name']
        room.description = request.POST['description']
        room.topic = topic
        room.save()
        # form = RoomForm(request.POST, instance = room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    
    return render(request,'socials/create-room.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    
    if request.method =='P0ST':
        room.delete()
        return redirect('home')
    return render(request, 'socials/delete.html',{'obj':room.name})
    
def deleteComment(request, pk):
    message = Message.objects.get(pk = pk)
    if request.user !=message.user:
        return HttpResponse('you are not allowed to delete this post')

    context = {'obj':message.body[:30]}
    print(request.method)
    if request.method == 'POST':
        Message.objects.filter(pk = pk).delete()
        return redirect('home') 
    return render(request, 'socials/delete.html',context)

def userProfile(request,pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    mesages = user.message_set.all()
    topic = Topic.objects.all()
    #rooms = Room.objects.filter(host = user )
    context = {'user':user, 'rooms':rooms, 'message':mesages, 'topics':topic}
    return render(request, 'socials/profile.html',context )
@login_required(login_url='login')
def updateUser(request,):
    user = request.user
    form = UserForm(instance= user)
    if form.is_valid():
        form.save()
        return redirect('profile', pk= user.id)

    context = {'user':user,'form':form}
    return render(request,'socials/edit-user.html',context)


def topicPage(request):
    q = request.GET.get('q')
    if q is None:
        topics = Topic.objects.all()
    else:
        topics = Topic.objects.filter(Q(title__icontains=q))
    return render(request,'socials/topics.html',{'topics':topics})
    