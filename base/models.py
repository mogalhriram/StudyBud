from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    
    def __str__(self) -> str:
        return self.body[:20]


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True, blank=True)
    title= models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                                     primary_key=True, editable=False)
     
    class Meta:
        ordering = ['-updated','-created',]

    def __str__(self) :
        return self.title

class Topic(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    def __str__(self):
        return self.name
