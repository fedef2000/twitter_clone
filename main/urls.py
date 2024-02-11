from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('home/', views.ListTweets.as_view(), name='tweet_list'),
    path('feed/', views.Feed.as_view(), name='feed'),
    path('tweet/<pk>/', views.DetailTweetView.as_view(), name='detail_tweet'),
    path('profile/<pk>/', views.ProfileDetailView.as_view(), name='detail_profile'),
    path('myprofile/', views.myProfile , name='my_profile'),
    path('createtweet/', views.CreateTweetView.as_view(), name='create_tweet'),
    path('updatetweet/<pk>/', views.UpdateTweetView.as_view(), name='update_tweet'),
    path('deletetweet/<pk>/', views.DeleteTweetView.as_view(), name='delete_tweet'),
    path('liketweet/', views.tweetLike, name="tweet_like"),
    path('updateprofile/<pk>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('follow/<int:pk>', views.follow, name="follow"),
    path("searchProfile/", views.search_profile, name="search_profile"),
    path("searchProfileResults/<str:name>/", views.SearchProfileResults.as_view(), name="search_profile_results"),
    path("searchTweet/", views.search_tweet, name="search_tweet"),
    path("searchTweetResults/<str:category>/<str:text>", views.SearchTweetResultsView.as_view(), name="search_tweet_results")
]

