from django.forms import ModelForm, ClearableFileInput, PasswordInput
from django import forms

from image_repository.models.image import Image
from image_repository.models.user import User


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User


class SignUpForm(ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'


class ImageUploadForm(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.ImageField()

    class Meta:
        model = Image
