from django.core.files import File

from main.models import *
from django.core.files.images import ImageFile


def erase_db():
    Profile.objects.all().delete()
    Tweet.objects.all().delete()
    UserFollowing.objects.all().delete()
    print("DB cancellato correttamente")


def init_db():
    if len(Profile.objects.all()) != 0:
        return
    if len(Tweet.objects.all()) != 0:
        return

    profiles = {
        "name": ["Alessandro Manzoni", "George Orwell", "Omero", "Alessandro Baricco", "Virgilio"],
        "email": ["manzoni@gmail.com", "orwell@gmail.com", "omero@gmail.com", "baricco@gmail.com",
                  "virgilio@gmail.com"],
        "password": ["12345678", "12345678", "12345678", "12345678", "12345678"],
    }

    # add new profiles
    for i in range(5):
        p = Profile()
        for k in profiles:
            if k == "name":
                p.name = profiles[k][i]
            if k == "email":
                p.email = profiles[k][i]
            if k == "password":
                p.password = profiles[k][i]
        try:
            p.save()
        except:
            print("errore durante il salvataggio")

    # make some user follow some other
    for i in range(4):
        user = Profile.objects.get(name=profiles["name"][i])
        follow = Profile.objects.get(name=profiles["name"][i + 1])
        UserFollowing.objects.create(user_id=user, following_user_id=follow)

    tweets = {
        "text": ["Lorem ipsum", "Sic transit gloria mundi", "Aleja iacta est", "Quid pro qui", "Vamonos"],
    }

    # create some tweets
    for i in range(5):
        t = Tweet()
        t.text = tweets["text"][i]
        user = Profile.objects.get(name=profiles["name"][i])
        t.user = user
        if i == 3:
            t.photo = "/defaultProfileImage.jpg"
        try:
            t.save()
        except:
            print("errore durante la creazione di un tweet")

    print("DUMP DB")
    print(Profile.objects.all())
    print(Tweet.objects.all())
