from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from main.models import Profile


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        profile = Profile()
        profile.user = user
        profile.name = user.username
        user.save()
        profile.save()

        print("inserito utente :" + str(user))
        print("inserito profilo :" + str(profile))
        return HttpResponseRedirect(self.success_url)


def handler404(request, exception):
    return render(request=request, template_name='404_handler.html')
