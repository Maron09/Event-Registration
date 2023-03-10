from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['details']


class CustomCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']