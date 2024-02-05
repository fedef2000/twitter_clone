from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main.forms import SearchForm
from main.models import Tweet, Profile


# Create your views here.
class ListTweets(ListView):
    model = Tweet
    template_name = "main/list_tweet.html"

    def get_queryset(self):
        return self.model.objects.order_by("-date")[:20]


class DetailTweetView(DetailView):
    model = Tweet
    template_name = "main/detail_tweet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweet'] = context["object"]
        return context


class CreateTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "main/create_tweet.html"
    fields = ["text", "photo"]
    success_url = reverse_lazy("main:tweet_list")

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.author = Profile.objects.get(user=User.objects.get(username=self.request.user))
        print("photo:")
        print(tweet.photo)
        tweet.save()
        return HttpResponseRedirect(self.success_url)


class UpdateTweetView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = "main/update_tweet.html"
    fields = ["text", "photo"]

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("main:detail_tweet", kwargs={'pk': pk})

    def get_object(self, *args, **kwargs):
        tweet = super(UpdateTweetView, self).get_object(*args, **kwargs)
        profile = Profile.objects.get(user=self.request.user)
        if not tweet.author == profile:
            raise Http404
        return tweet

    def form_valid(self, form):
        form.instance.owner_user = self.request.user
        return super(UpdateTweetView, self).form_valid(form)


class DeleteTweetView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = "main/delete_tweet.html"
    success_url = reverse_lazy("main:tweet_list")


def search_tweet(request, text):
    qs = Tweet.objects.filter(text__icontains=text)
    return render(request, template_name="main/search_tweet.html", context={"object_list": qs})


# Profile views
def search_profile_by_name(request, name):
    qs = Profile.objects.filter(name__icontains=name)
    return render(request, template_name="main/search_profile.html", context={"object_list": qs})


class ProfileDetailView(DetailView):
    model = User
    template_name = "main/detail_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = context["object"].pk
        user = User.objects.get(id=pk)
        profile = Profile.objects.get(user=user)
        tweets = Tweet.objects.filter(author=profile)
        context["profile"] = profile
        context['tweets'] = tweets
        return context


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("main:search_results", sstring, where)
    else:
        form = SearchForm()
    return render(request, template_name="main/search.html", context={"form": form})


class SearchResultsListView(ListView):
    model = Profile
    template_name = "main/search_results.html"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        where = self.request.resolver_match.kwargs["where"]

        if "Users" in where:
            return Profile.objects.filter(name__icontains=sstring)
        else:
            return Tweet.objects.filter(text__icontains=sstring)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        where = self.request.resolver_match.kwargs["where"]
        context['where'] = where
        return context
