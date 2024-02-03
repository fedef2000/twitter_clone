from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_pic', default='/defaultProfileImage.jpg', blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "user: " + self.user.__str__() + ", name: " + self.name


class Tweet(models.Model):
    text = models.TextField(max_length=500)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(default=timezone.now, blank=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    likedBy = models.ManyToManyField(Profile, related_name='likedTweet', blank=True)

    def __str__(self):
        return "id: " + str(self.id) + ", data:  " + str(self.date) + " - " + self.user.name + " - " + self.text


class UserFollowing(models.Model):
    user_id = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
