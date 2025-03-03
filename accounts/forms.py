from django.contrib.auth import forms

from .models import CustomUserModel


class CustomUserCreateForm(forms.UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ('username', 'email', 'gender', 'age')


class CustomUserChangeForm(forms.UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = ('username', 'email', 'gender', 'age')
