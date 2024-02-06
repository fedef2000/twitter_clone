from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
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
    context_object_name = 'tweets'

    def get_queryset(self):
        tweets = self.model.objects.order_by("-date")[:20]
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            for tweet in tweets:
                likes_connected = get_object_or_404(Tweet, id=tweet.id)
                liked = False
                if likes_connected.likedBy.filter(id=profile.id).exists():
                    liked = True
                tweet.number_of_likes = likes_connected.number_of_likes()
                tweet.post_is_liked = liked
        return tweets


class DetailTweetView(DetailView):
    model = Tweet
    template_name = "main/detail_tweet.html"
    context_object_name = 'tweet'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Tweet, id=self.kwargs['pk'])
        profile = Profile.objects.get(user=self.request.user)
        liked = False
        if likes_connected.likedBy.filter(id=profile.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


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
    else:
        return HttpResponseRedirect(reverse('main:detail_tweet', args=[str(pk)]))


def search_tweet(request, text):
    qs = Tweet.objects.filter(text__icontains=text).order_by("-date")
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
        profile = Profile.objects.get(user=User.objects.get(id=pk))
        tweets = Tweet.objects.filter(author=profile).order_by("-date")
        if self.request.user.is_authenticated:
            for tweet in tweets:
                user = User.objects.get(id=self.request.user.id)
                p = Profile.objects.get(user=user)
                likes_connected = get_object_or_404(Tweet, id=tweet.id)
                liked = False
                if likes_connected.likedBy.filter(id=p.id).exists():
                    liked = True
                tweet.number_of_likes = likes_connected.number_of_likes()
                tweet.post_is_liked = liked
        context["user"] = self.request.user # senza questa linea lo user nel template veniva impostato come quello di cui si stava visionando il profilo
        context["profile"] = profile
        context['tweets'] = tweets
        print(self.request.user.is_authenticated)
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
        return context
