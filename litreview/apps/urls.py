from . import views
from django.urls import path
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.connexion, name="login"),
    path('logout', views.deconnexion, name="logout"),
    path('flux', views.flux, name="flux"),
    path('posts', views.posts, name="posts"),
    path('subscription', views.subscription, name="subscription"),
    path('create_review', views.create_review, name="create_review"),
    path('add_review', views.add_review, name="add_review"),
    path('create_ticket', views.create_ticket, name="create_ticket"),
]
