from django.forms import ModelForm, modelformset_factory, Form, ModelChoiceField
from django.forms.widgets import TextInput, Textarea, FileInput, Select
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField, AuthenticationForm


from apps.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': TextInput(attrs={'placeholder': "Titre"}),
            'description': Textarea(attrs={'placeholder': "Description", "rows": 5, "cols": 20}),
            'image': FileInput(attrs={'placeholder': "Image"}),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'rating': TextInput(attrs={'placeholder': "Note"}),
            'headline': TextInput(attrs={'placeholder': "Titre"}),
            'body': Textarea(attrs={'placeholder': "Commentaire", "rows": 5, "cols": 20}),
        }


class UsersForm(Form):
    username = ModelChoiceField(
        queryset=User.objects.filter(groups__name='Community'))

    # def __init__(self, *args, **kwargs):
    #     pass
