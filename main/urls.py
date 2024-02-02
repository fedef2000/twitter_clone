from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('home/', views.ListTweets.as_view(), name='tweet_list'),
    path('tweet/<pk>/', views.DetailTweetView.as_view(), name='detail_tweet'),
    path('profile/<pk>/', views.ProfileDetailView.as_view(), name='detail_profile'),
    path('createtweet/', views.CreateTweetView.as_view(), name='create_tweet'),
    path('updatetweet/<pk>/', views.UpdateTweetView.as_view(), name='update_tweet'),
    path('deletetweet/<pk>/', views.DeleteTweetView.as_view(), name='delete_tweet'),
    #path('profilesearch/<str:name>/', views.search_profile_by_name, name='search_profile_by_name'),
    #path('tweetsearch/<str:text>/', views.search_tweet, name='search_tweet'),
    path("search/", views.search, name="search"),
    path("searchresults/<str:sstring>/<str:where>/", views.SearchResultsListView.as_view(), name="search_results")

]

