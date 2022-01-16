from django import forms

from image_repository.models.image import Image
from image_repository.models.user import User


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


class ImageUploadForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    options = (
        (Image.Permission.PRIVATE, Image.Permission.PRIVATE),
        (Image.Permission.PUBLIC, Image.Permission.PUBLIC),
    )
    permission = forms.CharField(widget=forms.Select(choices=options))

    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class ImageSearchForm(forms.ModelForm):
    height = forms.IntegerField(required=False, initial=0)
    width = forms.IntegerField(required=False, initial=0)
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))

    class Meta:
        model = Image
        fields = ['color', 'permission']