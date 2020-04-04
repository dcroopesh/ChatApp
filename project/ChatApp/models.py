from django.db import models
from django.contrib.auth.models import User

class chatapp(models.Model):
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=30)
    roomname = models.CharField(max_length=10)

class p2p(models.Model):
    
    username = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    message = models.CharField(max_length=30)
    roomname = models.CharField(max_length=10)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sent")

class room(models.Model):
    user = models.CharField(max_length=10) 
