import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Tweet, Profile, UserFollowing


# Create your tests here.
def create_user(username, email, password):
    return User.objects.create_user(username=username, email=email, password=password)


def create_profile(user, name):
    return Profile.objects.create(user=user, name=name)


def create_tweet(author, text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Tweet.objects.create(author=author, text=text, date=time)


def create_follower(follower, following):
    UserFollowing.objects.create(profile=follower, following=following)


class TweetListViewTests(TestCase):
    def test_tweet_list_view_with_no_tweet(self):
        response = self.client.get(reverse('main:tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non ci sono tweet da mostrare")
        self.assertQuerysetEqual(response.context['tweets'], [])

    def test_tweet_list_view_with_a_past_tweet(self):
        user = create_user(username="user", email="EMAIL", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        tweet = create_tweet(text="text", days=-30, author=profile)
        response = self.client.get(reverse('main:tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tweet in response.context['tweets'])

    def test_tweet_list_view_with_a_future_tweet(self):
        user = create_user(username="user", email="EMAIL", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        tweet = create_tweet(text="text", days=30, author=profile)
        response = self.client.get(reverse('main:tweet_list'))
        self.assertTrue(tweet not in response.context['tweets'])
        self.assertEqual(response.status_code, 200)

    def test_tweet_list_view_with_future_and_past_tweet(self):
        user = create_user(username="user", email="EMAIL", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        past_tweet = create_tweet(text="Past", days=-30, author=profile)
        future_tweet = create_tweet(text="Future", days=30, author=profile)
        response = self.client.get(reverse('main:tweet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(past_tweet in response.context['tweets'] and future_tweet not in response.context['tweets'])


class FeedViewTests(TestCase):
    def test_feed_with_no_tweets(self):
        user = create_user(username="user", email="EMAIL", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        self.client.login(username='user', password='PASSWORD')
        response = self.client.get(reverse('main:feed', ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non ci sono tweet da mostrare")

    def test_feed_with_tweet(self):
        tweet_author_user = create_user(username="user1", email="EMAIL1", password="PASSWORD")
        tweet_author_profile = create_profile(user=tweet_author_user, name="user")
        tweet = create_tweet(author=tweet_author_profile, text="text", days=-30)
        user = create_user(username="user2", email="EMAIL2", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        create_follower(profile, tweet_author_profile)
        self.client.login(username='user2', password='PASSWORD')
        response = self.client.get(reverse('main:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tweet in response.context['tweets'])

    def test_feed_with_future_tweet(self):
        tweet_author_user = create_user(username="user1", email="EMAIL1", password="PASSWORD")
        tweet_author_profile = create_profile(user=tweet_author_user, name="user")
        tweet = create_tweet(author=tweet_author_profile, text="text", days=30)
        user = create_user(username="user2", email="EMAIL2", password="PASSWORD")
        profile = create_profile(user=user, name="user")
        create_follower(profile, tweet_author_profile)
        self.client.login(username='user2', password='PASSWORD')
        response = self.client.get(reverse('main:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tweet not in response.context['tweets'])
