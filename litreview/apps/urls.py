from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.connexion, name="login"),
    path('logout', views.deconnexion, name="logout"),
    path('flux', views.flux, name="flux"),
    path('posts', views.posts, name="posts"),
    path('subscription', views.subscription, name="subscription"),
    path('unsubscription', views.unsubscription, name="unsubscription"),
    path('create_ticket', views.create_ticket, name="create_ticket"),
    path('update_ticket/<int:id>', views.update_ticket, name="update_ticket"),
    path('delete_ticket/<int:id>', views.delete_ticket, name="delete_ticket"),
    path('create_review', views.create_review, name="create_review"),
    path('view_review/<int:id>', views.view_review, name="view_review"),
    path('add_review', views.add_review, name="add_review"),
    path('update_review/<int:id>', views.update_review, name="update_review"),
    path('delete_review/<int:id>', views.delete_review, name="delete_review"),
]
