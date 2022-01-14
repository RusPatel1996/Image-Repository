from django.forms import ModelForm, ClearableFileInput, PasswordInput

from image_repository.models.image import Image
from image_repository.models.user import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']
        widgets = {
            'password': PasswordInput()
        }


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': PasswordInput()
        }


class MultipleImageAddingForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        widgets = {
            'media': ClearableFileInput(attrs={'multiple': True})
        }
