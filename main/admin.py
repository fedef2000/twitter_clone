from django.contrib import admin

from main.models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(UserFollowing)
