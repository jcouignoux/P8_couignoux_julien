from . import views
from django.urls import path
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.connexion, name="login"),
    path('logout', views.deconnexion, name="logout"),
    path('flux', views.flux, name="flux"),
    path('subscription', views.subscription, name="subscription"),
    path('post', views.post, name="post"),
]
