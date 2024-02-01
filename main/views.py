from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import *

from main.models import Tweet


# Create your views here.
class ListTweets(ListView):
    model = Tweet
    template_name = "main/list_tweet.html"

    def get_queryset(self):
        return self.model.objects.order_by("date")[:20]


class DetailTweets(DetailView):
    model = Tweet
    template_name = "main/detail_tweet.html"


class CreateTweetView(CreateView):
    model = Tweet
    template_name = "main/create_tweet.html"
    fields = "__all__"
    success_url = reverse_lazy("main:tweet_list")


class UpdateTweetView(UpdateView):
    model = Tweet
    template_name = "main/update_tweet.html"
    fields = ["text"]

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("main:detail_tweet", kwargs={'pk': pk})


class DeleteTweetView(DeleteView):
    model = Tweet
    template_name = "main/delete_tweet.html"
    success_url = reverse_lazy("main:tweet_list")