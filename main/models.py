from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_photo', default='defaultProfileImage.jpg', blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "user: " + self.user.__str__() + ", name: " + self.name + ", tweets: " + str(self.tweets)


class Tweet(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tweets')
    date = models.DateTimeField(default=timezone.now, blank=True)
    photo = models.ImageField(upload_to='tweet_photo', blank=True, null=True)
    likedBy = models.ManyToManyField(Profile, related_name='likedTweet', blank=True)

    def number_of_likes(self):
        return self.likedBy.count()

    def __str__(self):
        return "id: " + str(self.id) + ", data:  " + str(self.date) + " - " + self.author.name + " - " + self.text


class UserFollowing(models.Model):
    profile = models.ForeignKey(Profile, related_name="followings", on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def is_following(self, profile):
        if self.profile == profile:
            return True
        return False
