from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from main.forms import ProfileUpdateForm, SearchTweetForm, SearchProfileForm
from main.models import Tweet, Profile, UserFollowing


# Create your views here.
class ListTweets(ListView):
    model = Tweet
    template_name = "main/list_tweet.html"
    context_object_name = 'tweets'

    def get_queryset(self):
        tweets = self.model.objects.filter(date__lte=timezone.now()).order_by("-date")[:20]
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
        return tweets.filter(date__lte=timezone.now()).order_by("-date")


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
    fields = ["text", "photo", "category"]
    success_url = reverse_lazy("main:tweet_list")

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.author = Profile.objects.get(user=User.objects.get(username=self.request.user))
        tweet.save()
        messages.success(self.request, 'Tweet creato con successo')
        return HttpResponseRedirect(self.success_url)


class UpdateTweetView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = "main/update_tweet.html"
    fields = ["text", "photo", "category"]

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("main:detail_tweet", kwargs={'pk': pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Tweet modificato con successo')
        return HttpResponseRedirect(self.get_success_url())


class DeleteTweetView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = "main/delete_tweet.html"
    success_url = reverse_lazy("main:tweet_list")

    def form_valid(self, form):
        self.get_object().delete()
        messages.success(self.request, 'Tweet cancellato con successo')
        return HttpResponseRedirect(self.success_url)


def tweetLike(request, pk, page):
    tweet = get_object_or_404(Tweet, id=request.POST.get('tweet_id'))
    profile = Profile.objects.get(user=request.user)
    if tweet.likedBy.filter(id=profile.id).exists():
        tweet.likedBy.remove(profile)
    else:
        tweet.likedBy.add(profile)

    if page == "Profile":
        return HttpResponseRedirect(reverse('main:detail_profile', args=[str(pk)]))
    elif page == "Feed":
        return HttpResponseRedirect(reverse('main:feed'))
    elif page == "Tweet":
        return HttpResponseRedirect(reverse('main:detail_tweet', args=[str(pk)]))
    else:
        return HttpResponseRedirect(reverse('main:tweet_list'))


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
        context[
            "user"] = self.request.user  # senza questa linea lo user nel template veniva impostato come quello di cui si stava visionando il profilo
        context["profile"] = profile
        context['tweets'] = tweets
        return context


def search_profile(request):
    if request.method == "POST":
        form = SearchProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            return redirect("main:search_profile_results", name)
    else:
        form = SearchProfileForm()
    return render(request, template_name="main/search_profile.html", context={"form": form})


class SearchProfileResults(ListView):
    model = Profile
    template_name = "main/search_profile_results.html"

    def get_queryset(self):
        name = self.request.resolver_match.kwargs["name"]
        return Profile.objects.filter(name__icontains=name)


def search_tweet(request):
    if request.method == "POST":
        form = SearchTweetForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            text = form.cleaned_data.get("text")
            if text == "":
                text = " "
            return redirect("main:search_tweet_results",  category=category, text=text)
    else:
        form = SearchTweetForm()
    return render(request, template_name="main/search_tweet.html", context={"form": form})


class SearchTweetView(ListView):
    model = Tweet
    template_name = "main/search_tweet_results.html"

    def get_queryset(self):
        category = self.request.resolver_match.kwargs["category"]
        text = self.request.resolver_match.kwargs["text"]
        if text == " ":
            return Tweet.objects.filter(category__icontains=category).order_by("-date")
        else:
            return Tweet.objects.filter(text__icontains=text, category__icontains=category).order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.request.resolver_match.kwargs["category"]
        context["tweets"] = context["object_list"]
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            for tweet in context["tweets"]:
                tweet.post_is_liked = tweet.likedBy.filter(id=profile.id).exists()

        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "main/update_profile.html"
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse("main:detail_profile", kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        profile = form.save(commit=False)
        if not profile.photo:
            profile.photo = "defaultProfileImage.jpg"
        profile.save()
        messages.success(self.request, 'Profilo aggiornato con successo')
        return HttpResponseRedirect(self.get_success_url())


def follow(request, pk):
    profile = Profile.objects.get(user=request.user)
    following = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    if UserFollowing.objects.filter(profile=profile, following=following).exists():
        UserFollowing.objects.filter(profile=profile, following=following).delete()
    else:
        UserFollowing.objects.create(profile=profile, following=following)

    return HttpResponseRedirect(reverse('main:detail_profile', args=[str(pk)]))
