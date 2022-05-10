import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from apps.forms import UserForm
# Create your views here.


def index(request):

    if request.user.is_authenticated:
        return render(request, 'apps/index.html')
    else:
        # AForm = AuthenticationForm()
        # context = {'AForm': AForm}
        # return render(request, 'apps/login.html', context)
        return redirect(reverse('apps:login'))


def signup(request):

    if request.method == "POST":
        UForm = UserCreationForm(request, data=request.POST or None)
        if UForm.is_valid():
            UForm.save()
    UForm = UserCreationForm()
    context = {'UForm': UForm}

    return render(request, 'apps/signup.html', context)


def flux(request):

    return render(request, 'apps/flux.html')


def subscription(request):

    return render(request, 'apps/subscription.html')


def post(request):

    return render(request, 'apps/post.html')


def connexion(request):

    context = {}
    AForm = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if AForm.is_valid():
            username = AForm.cleaned_data['username']
            password = AForm.cleaned_data['password']
            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('apps:index'))
            else:
                error_message = "Identifiant ou mot de passe incorrect."
                messages.error(request, error_message)
    else:
        context['AForm'] = AForm

    return render(request, 'apps/login.html', context)


def deconnexion(request):

    logout(request)

    return redirect(reverse('apps:index'))
