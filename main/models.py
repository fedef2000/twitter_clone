from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_pic', default='defaultProfileImage.jpg', blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    follow = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return "nome: " + self.name + " email: " + self.email


class Tweet(models.Model):
    text = models.TextField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(default=timezone.now, blank=True)
    photo = models.ImageField(upload_to='profile_pic', blank=True, null=True)
    likedBy = models.ManyToManyField(Profile, related_name='likedTweet', blank=True)

    def __str__(self):
        return str(self.date) + " - " + self.user.name + " - " + self.text
