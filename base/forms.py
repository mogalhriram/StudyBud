from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from .models import Room, Message
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']