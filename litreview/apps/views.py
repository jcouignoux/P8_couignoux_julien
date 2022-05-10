from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from apps.forms import TicketForm, ReviewForm, UsersFormSet, UsersForm
from apps.models import Ticket, UserFollows
# Create your views here.


def index(request):

    if request.user.is_authenticated:
        return render(request, 'apps/index.html')
    else:
        return redirect(reverse('apps:login'))


@login_required
def flux(request):

    context = {}

    tickets_list = Ticket.objects.all().order_by('-time_created')
    context['tickets'] = tickets_list

    return render(request, 'apps/flux.html', context)


@login_required
def posts(request):

    context = {}

    tickets_list = Ticket.objects.filter(user=request.user)
    context['tickets'] = tickets_list

    return render(request, 'apps/posts.html', context)


@login_required
def subscription(request):

    context = {}

    if request.method == "POST":
        UForm = UsersForm(request.POST or None)
        if UForm.is_valid():
            username = UForm.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                userFollows = UserFollows()
                userFollows.user = request.user
                userFollows.followed_user = user
                userFollows.save()
            else:
                error_message = "Username inconnu."
                messages.error(request, error_message)

    UForm = UsersForm()
    following_users = UserFollows.objects.filter(user=request.user)
    followed_users = UserFollows.objects.filter(followed_user=request.user)

    context['UForm'] = UForm
    context['following_users'] = following_users
    context['followed_users'] = followed_users

    return render(request, 'apps/subscription.html', context)


@login_required
def ticket(request):

    context = {}

    TForm = TicketForm(request.POST or None)
    RForm = ReviewForm(request.POST or None)
    if request.method == "POST":
        if TForm.is_valid() and RForm.is_valid():
            ticket = TForm.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = RForm.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

    context['TForm'] = TForm
    context['RForm'] = RForm
    tickets_list = Ticket.objects.filter(user=request.user)
    context['tickets'] = tickets_list

    return render(request, 'apps/ticket.html', context)


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
