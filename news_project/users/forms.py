from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    '''
    Form to create a new user with a custom role.

    :param data: Optional form submission data.
    :return: Validated CustomUser instance.
    '''
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "email", "role"]
