from django.forms import ModelForm, ClearableFileInput, PasswordInput
from django import forms

from image_repository.models.image import Image
from image_repository.models.user import User


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User


class UserRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'


class MultipleImageAddingForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        widgets = {
            'media': ClearableFileInput(attrs={'multiple': True})
        }
