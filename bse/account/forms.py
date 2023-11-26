from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

UserModel = get_user_model()


class UserRegisterForm(UserCreationForm):
    consent = forms.BooleanField()

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2', 'consent')
        error_messages = {
            'username': {
                'unique': 'This username is already taken',
            },
            'email': {
                'unique': 'User with this email already exists'
            },
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Repeat password'
        }
