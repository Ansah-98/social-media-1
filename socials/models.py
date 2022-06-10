from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length= 100)
    
    def __str__(self):
        return self.title

class Room(models.Model):
    #participants =models.ManyToManyField(User,null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True, blank= True )
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank= True,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length= 300 ,null= True, blank= True )
    room = models.ForeignKey(Room, on_delete = models.CASCADE,)
    created = models.DateTimeField(auto_now_add =True  )
    updated = models.DateTimeField(auto_now=True )

    def __str__(self):
        return self.body[:50]