import datetime
import random

from main.models import *
from django.contrib.auth.models import User


def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)


def create_profile(user, name):
    return Profile.objects.create(user=user, name=name)


def create_tweet(author, text, category, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Tweet.objects.create(author=author, text=text, date=time, category=category)


def create_follower(follower, following):
    UserFollowing.objects.create(profile=follower, following=following)


def erase_db():
    User.objects.all().delete()
    Profile.objects.all().delete()
    Tweet.objects.all().delete()
    UserFollowing.objects.all().delete()
    print("DB cancellato correttamente")


def init_db():

    profiles = {
        "name": ["Francesco Castagnoli", "George Orwell", "Paolo Rossi", "Alessandro Baricco", "Vincenzo Virgilio"],
        "email": ["FraCasta@gmail.com", "orwell@gmail.com", "PRossi@gmail.com", "baricco@gmail.com",
                  "virgilio@gmail.com"],
        "password": ["12345678", "12345678", "12345678", "12345678", "12345678"],
    }
    tweets = {
        "text": ["Il mio sport preferito è il basket", "Alle prossime elezioni non andrò a votare", "Fellini è il miglior regista di sempre", "Ascoltate il nuovo album di Calcutta", "Domani partirò per la Thailandia", "Ho appena comprato il nuovo Iphone", "Oggi si guarda masterchef", "Al museo a guardare Monet", "Guardate che bella foto"],
        "category": ["Sport", "Politica", "Cinema", "Musica", "Viaggi", "Tecnologia", "Cucina", "Arte", "Fotografia"]

    }

    # add a superuser
    user = User.objects.create_superuser(username="fede", email="fede@gmail.com", password="fede")
    create_profile(user=user, name="Federico Ferrari")

    for i in range(5):
        try:
            user = create_user(username=profiles["name"][i], email=profiles["email"][i], password=profiles["password"][i])
            create_profile(user=user, name=profiles["name"][i])
        except Exception as e:
            print(e)

    for i, profile in enumerate(Profile.objects.all()):
        for j in range(i):
            n = random.randint(0,8)
            create_tweet(profile, tweets["text"][n], tweets["category"][n], -5)

    print("DUMP DB")
    print(Profile.objects.all())
    print(Tweet.objects.all())
