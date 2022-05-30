import re
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from apps.forms import TicketForm, ReviewForm, UsersForm
from apps.models import Ticket, Review, UserFollows
from apps.post import get_all_posts
# Create your views here.


def index(request):

    if request.user.is_authenticated:
        return render(request, 'apps/index.html')
    else:
        return redirect(reverse('apps:login'))


@login_required
def flux(request):

    context = {}

    users = [u.followed_user for u in UserFollows.objects.filter(
        user=request.user)]
    RForm = ReviewForm()
    posts_list = get_all_posts(users)

    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    context['paginate'] = True
    context['posts'] = posts_list
    context['RForm'] = RForm

    return render(request, 'apps/flux.html', context)


@login_required
def posts(request):

    context = {}

    RForm = ReviewForm(request.POST or None)
    posts_list = get_all_posts(users=[request.user])
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    context['paginate'] = True
    context['posts'] = posts_list
    context['RForm'] = RForm

    return render(request, 'apps/posts.html', context)


@login_required
def subscription(request):

    context = {}

    if request.method == "POST":
        UForm = UsersForm(user=request.user, data=request.POST)
        if UForm.is_valid():
            username = UForm.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            try:
                if user:
                    userFollows = UserFollows()
                    userFollows.user = request.user
                    userFollows.followed_user = user
                    userFollows.save()
                    success = str(userFollows.followed_user) + " ajouté."
                    messages.success(request, success)
            except Exception as e:
                messages.error(request, e)

    UForm = UsersForm(user=request.user)
    following_users = UserFollows.objects.filter(user=request.user)
    followed_users = UserFollows.objects.filter(followed_user=request.user)

    context['UForm'] = UForm
    context['following_users'] = following_users
    context['followed_users'] = followed_users

    return render(request, 'apps/subscription.html', context)


@login_required
def unsubscription(request):

    if request.method == "POST":
        followed_user_id = request.POST.get('followed_user_id')
        followed_user = get_object_or_404(User, pk=followed_user_id)
        if followed_user:
            UserFollows.objects.filter(
                user=request.user, followed_user=followed_user).delete()

    return redirect(reverse('apps:subscription'))


@login_required
def create_ticket(request):

    context = {}
    context['title'] = 'Créer un ticket'

    if request.method == "POST":
        TForm = TicketForm(request.POST, request.FILES)
        if TForm.is_valid():
            try:
                ticket = TForm.save(commit=False)
                ticket.user = request.user
                ticket.save()
                print(TForm)
                messages.success(request, "Demande de critique créée.")
            except Exception as e:
                messages.error(request, e)

        return redirect(reverse('apps:flux'))
    else:
        TForm = TicketForm()

    context['TForm'] = TForm

    return render(request, 'apps/ticket.html', context)


@login_required
def update_ticket(request, id):

    context = {}
    context['title'] = 'Modifier un ticket'
    ticket = get_object_or_404(Ticket, pk=id)
    context['ticket'] = ticket

    if request.method == "POST":
        TForm = TicketForm(request.POST, request.FILES, instance=ticket)
        TForm.save()

        return redirect(reverse('apps:posts'))

    else:
        TForm = TicketForm(instance=ticket)

    context['TForm'] = TForm

    return render(request, 'apps/ticket.html', context)


@login_required
def delete_ticket(request, id):

    ticket = get_object_or_404(Ticket, pk=id)

    if request.method == "POST":
        ticket.image.delete()
        ticket.delete()

    return redirect(reverse('apps:posts'))


@ login_required
def add_review(request):

    context = {}

    RForm = ReviewForm(request.POST or None)
    if request.method == "POST":
        try:
            ticket_id = request.POST.get('post_id')
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            review = Review()
            rating = request.POST.get('val_star')
            review.headline = RForm.data['headline']
            review.body = RForm.data['body']
            review.rating = rating
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Critique Créée.")
        except Exception as e:
            messages.error(request, e)

        return redirect(reverse('apps:flux'))

    context['RForm'] = RForm

    return render(request, 'apps/review.html', context)


@ login_required
def view_review(request, id):

    context = {}
    RForm = ReviewForm()
    review = get_object_or_404(Review, pk=id)
    context['post'] = review
    context['RForm'] = RForm

    return render(request, 'apps/review_item.html', context)


@ login_required
def update_review(request, id):

    context = {}
    context['title'] = 'Modifier une critique'
    review = get_object_or_404(Review, pk=id)
    context['review'] = review
    context['ticket'] = review.ticket

    if request.method == "POST":
        try:
            RForm = ReviewForm(request.POST, instance=review)
            rating = request.POST.get('val_star')
            review.headline = RForm.data['headline']
            review.body = RForm.data['body']
            review.rating = rating
            review.save()
            messages.success(request, "Critique modifiée.")
        except Exception as e:
            messages.error(request, e)

        return redirect(reverse('apps:posts'))
    else:
        RForm = ReviewForm(instance=review)

    context['RForm'] = RForm

    return render(request, 'apps/review.html', context)


@ login_required
def create_review(request):

    context = {}
    context['title'] = 'Créer une critique'

    if request.method == "POST":
        TForm = TicketForm(request.POST, request.FILES)
        RForm = ReviewForm(request.POST)
        if TForm.is_valid():
            try:
                ticket = TForm.save(commit=False)
                ticket.user = request.user
                ticket.image = request.FILES.get('image')
                print(TForm)
                ticket.save()
                review = Review()
                rating = request.POST.get('val_star')
                review.headline = RForm.data['headline']
                review.body = RForm.data['body']
                review.rating = rating
                review.user = request.user
                review.ticket = ticket
                review.save()
                messages.success(request, "Critique créée.")
            except Exception as e:
                messages.error(request, e)

            return redirect(reverse('apps:flux'))
    else:
        TForm = TicketForm()
        RForm = ReviewForm()

    context['TForm'] = TForm
    context['RForm'] = RForm

    return render(request, 'apps/review.html', context)


@login_required
def delete_review(request, id):

    review = get_object_or_404(Review, pk=id)

    if request.method == "POST":
        review.delete()

    return redirect(reverse('apps:posts'))


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
                return redirect(reverse('apps:flux'))
            else:
                error_message = "Identifiant ou mot de passe incorrect."
                messages.error(request, error_message)
        context['AForm'] = AForm
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
