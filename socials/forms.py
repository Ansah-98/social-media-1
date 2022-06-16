from pyexpat import model
from django.forms import ModelForm
from .models import Room,Message,Topic,User


class RoomForm(ModelForm):
    class Meta:
        model= Room
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields=['profile_img','name','username','bio']
