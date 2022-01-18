from django import forms

from image_repository.models.image import Image
from image_repository.models.user import User

from django.core.exceptions import ValidationError


def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }


class ImageUploadForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    options = (
        (Image.Permission.PRIVATE, Image.Permission.PRIVATE),
        (Image.Permission.PUBLIC, Image.Permission.PUBLIC),
    )
    permission = forms.CharField(widget=forms.Select(choices=options))
    image = forms.ImageField(validators=[file_size], widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image


class ImageSearchForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    height = forms.IntegerField(required=False, initial=0)
    width = forms.IntegerField(required=False, initial=0)
    image = forms.ImageField(required=False)
    options = (
        ('none', '------'),
        ('name', 'Name'),
        ('height', 'Height'),
        ('width', 'Width'),
        ('color', 'Color'),
    )
    sort_criteria = forms.CharField(widget=forms.Select(choices=options))

    class Meta:
        model = Image
        fields = ['permission', 'color']
