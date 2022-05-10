from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
            'password': PasswordInput(attrs={'placeholder': "Mot de Passe"}),
            'email': EmailInput(attrs={'placeholder': "Email"}),
        }
