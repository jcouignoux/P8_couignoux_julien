from django.forms import ModelForm, Form, ModelChoiceField
from django.forms.widgets import TextInput, Textarea, FileInput, NumberInput
from django.contrib.auth.models import User

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
            'rating': NumberInput(),
            'headline': TextInput(attrs={'placeholder': "Titre"}),
            'body': Textarea(attrs={'placeholder': "Commentaire", "rows": 5, "cols": 20}),
        }


class UsersForm(Form):
    username = ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        self.fields['username'].queryset = User.objects.filter(
            groups__name='Community').exclude(followed_by__in=list(user.following.all())).exclude(id=user.id)
