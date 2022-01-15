from functools import wraps

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

# Create your views here.
from image_repository.forms import UserRegistrationForm, MultipleImageAddingForm, LoginForm
from image_repository.models.user import User, UserManager
from image_repository.models.image import Image, ImageManager

MAX_INT = 2 ** 31 - 1
MIN_INT = -2 ** 31


def index(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Do something

            return HttpResponseRedirect(reverse('image_repository:home'))
    else:
        login_form = LoginForm()
    return render(request, 'image_repository/index.html', {'login_form': login_form})


def home(request):
    return render(request, 'image_repository/home.html')


def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            manager = UserManager()
            data = user_form.cleaned_data
            user_name = data.get('user_name')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            manager.get_or_create_user(user_name=user_name, password=password, first_name=first_name, last_name=last_name)
            return HttpResponseRedirect(reverse('image_repository:index'))
    else:
        user_form = UserRegistrationForm()
    return render(request, 'image_repository/signup.html', {'form': user_form})


# def signup_redirect(request):
#     pass


def within_bounds(number):
    if MIN_INT <= int(number) <= MAX_INT:
        return True
    return False
