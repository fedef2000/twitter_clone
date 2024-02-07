from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from main.forms import SearchForm
from main.models import Tweet, Profile, UserFollowing


# Create your views here.
class ListTweets(ListView):
    model = Tweet
    template_name = "main/list_tweet.html"
    context_object_name = 'tweets'

    def get_queryset(self):
        tweets = self.model.objects.order_by("-date")[:20]
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            for tweet in tweets:
                tweet.post_is_liked = tweet.likedBy.filter(id=profile.id).exists()
        return tweets


class Feed(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "main/feed.html"
    context_object_name = 'tweets'

    def get_queryset(self):
        tweets = Tweet.objects.none()
        profile = Profile.objects.get(user=self.request.user)
        for p in profile.followings.all():
            if Tweet.objects.filter(author=p.following).exists():
                tweets |= Tweet.objects.filter(author=p.following)
            for tweet in tweets:
                tweet.post_is_liked = tweet.likedBy.filter(id=profile.id).exists()
        return tweets.order_by("-date")


class DetailTweetView(DetailView):
    model = Tweet
    template_name = "main/detail_tweet.html"
    context_object_name = 'tweet'

    def get_object(self, **kwargs):
        tweet = super(DetailTweetView, self).get_object()
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            tweet.post_is_liked = tweet.likedBy.filter(id=profile.id).exists()
        return tweet


class CreateTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "main/create_tweet.html"
    fields = ["text", "photo"]
    success_url = reverse_lazy("main:tweet_list")

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.author = Profile.objects.get(user=User.objects.get(username=self.request.user))
        tweet.save()
        return HttpResponseRedirect(self.success_url)


class UpdateTweetView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = "main/update_tweet.html"
    fields = ["text", "photo"]

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("main:detail_tweet", kwargs={'pk': pk})


class DeleteTweetView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = "main/delete_tweet.html"
    success_url = reverse_lazy("main:tweet_list")


def tweetLike(request, pk, page):
    tweet = get_object_or_404(Tweet, id=request.POST.get('tweet_id'))
    profile = Profile.objects.get(user=request.user)
    if tweet.likedBy.filter(id=profile.id).exists():
        tweet.likedBy.remove(profile)
    else:
        tweet.likedBy.add(profile)

    if page == "Home":
        return HttpResponseRedirect(reverse('main:tweet_list'))
    elif page == "Profile":
        return HttpResponseRedirect(reverse('main:detail_profile', args=[str(pk)]))
    elif page == "Feed":
        return HttpResponseRedirect(reverse('main:feed'))
    else:
        return HttpResponseRedirect(reverse('main:detail_tweet', args=[str(pk)]))


class ProfileDetailView(DetailView):
    model = User
    template_name = "main/detail_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = context["object"].pk
        profile = Profile.objects.get(user=User.objects.get(id=pk))
        tweets = Tweet.objects.filter(author=profile).order_by("-date")
        if self.request.user.is_authenticated:
            user = User.objects.get(id=self.request.user.id)
            p = Profile.objects.get(user=user)
            for tweet in tweets:
                tweet.post_is_liked = tweet.likedBy.filter(id=p.id).exists()
            if UserFollowing.objects.filter(profile=p, following=profile).exists():
                context["is_following"] = True
            else:
                context["is_following"] = False
        context["user"] = self.request.user  # senza questa linea lo user nel template veniva impostato come quello di cui si stava visionando il profilo
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
            return Tweet.objects.filter(text__icontains=sstring).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        where = self.request.resolver_match.kwargs["where"]
        context['where'] = where
        if where == "Tweets":
            context["tweets"] = context["object_list"]
            if self.request.user.is_authenticated:
                profile = Profile.objects.get(user=self.request.user)
                for tweet in context["tweets"]:
                    tweet.post_is_liked = tweet.likedBy.filter(id=profile.id).exists()

        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "main/update_profile.html"
    fields = ["name", "photo", "bio"]

    def get_success_url(self):
        return reverse("main:detail_profile", kwargs={'pk': self.request.user.id})


def follow(request, pk):
    profile = Profile.objects.get(user=request.user)
    following = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    if UserFollowing.objects.filter(profile=profile, following=following).exists():
        UserFollowing.objects.filter(profile=profile, following=following).delete()
    else:
        UserFollowing.objects.create(profile=profile, following=following)

    return HttpResponseRedirect(reverse('main:detail_profile', args=[str(pk)]))
