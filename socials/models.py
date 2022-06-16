from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique= True ,null=True)
    bio = models.TextField(max_length=300, null=True ,blank =True)
    profile_img= models.ImageField(null=True ,default ='avatar.svg')
    USERNAME_FIELD=  'email'
    REQUIRED_FIELDS = []
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
    participants = models.ManyToManyField(User, related_name='participants' ,blank= True)
    class Meta:
        ordering =['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length= 300 ,null= True, blank= True )
    room = models.ForeignKey(Room, on_delete = models.CASCADE,)
    created = models.DateTimeField(auto_now_add =True  )
    updated = models.DateTimeField(auto_now=True )

    def __str__(self):
        return self.body[:50]