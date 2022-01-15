import io

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from image_repository.forms import UserRegistrationForm, MultipleImageAddingForm, LoginForm
from image_repository.models.user import User, UserManager
from image_repository.models.image import Image, ImageManager
from utils.encrypt import Encryption
from image_repository.serializer import UserSerializer

MAX_INT = 2 ** 31 - 1
MIN_INT = -2 ** 31


def index(request):
    return HttpResponseRedirect('login')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            manager = UserManager()
            data = login_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            user = manager.login_user(user_name, password)
            if user:
                encrypted_user_name = Encryption.encrypt(user_name).decode()
                return HttpResponseRedirect(reverse('image_repository:home', args=(encrypted_user_name,)))
    else:
        login_form = LoginForm()
    return render(request, 'image_repository/index.html', {'login_form': login_form})


def home(request, user_name):
    manager = UserManager()
    user_name = Encryption.decrypt(user_name.encode())
    user = UserManager.get_user(user_name)
    return render(request, 'image_repository/home.html', {
        'user_name': user.first_name,
    })


def signup(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            manager = UserManager()
            data = user_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user = manager.get_or_create_user(user_name, password, first_name, last_name)
            messages.success(request, 'Sign up successful')
            return HttpResponseRedirect(reverse('image_repository:login'))
    else:
        user_form = UserRegistrationForm()
    return render(request, 'image_repository/signup.html', {'form': user_form})


def within_bounds(number):
    if MIN_INT <= int(number) <= MAX_INT:
        return True
    return False
