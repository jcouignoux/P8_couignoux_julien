from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.


def index(request):

    if request.user.is_authenticated:
        return render(request, 'apps/index.html')
    else:
        return redirect(reverse('apps:login'))


def signup(request):

    UForm = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if UForm.is_valid():
            user = UForm.save()
            group = Group.objects.get(name='Community')
            group.user_set.add(user)
            return redirect(reverse('apps:login'))
        else:
            error_message = "Identifiant ou mot de passe incorrect."
            messages.error(request, error_message)

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
        AForm = AuthenticationForm(request)
        context['AForm'] = AForm

    return render(request, 'apps/login.html', context)


def deconnexion(request):

    logout(request)

    return redirect(reverse('apps:index'))
