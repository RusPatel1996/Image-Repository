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
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }


class ImageUploadForm(ModelForm):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))

    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }


class ImageSearchForm(forms.Form):
    height = forms.IntegerField(required=False)
    width = forms.IntegerField(required=False)
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    image = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))

    class Meta:
        model = Image
