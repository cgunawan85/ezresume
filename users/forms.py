from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That username is already taken")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if validate_password(password1):
            raise forms.ValidationError('This password is not valid')
        return password1

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match! Please try again")
        return super(UserCreationForm, self).clean(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
