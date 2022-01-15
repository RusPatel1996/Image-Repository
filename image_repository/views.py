from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from image_repository.forms import SignUpForm, LoginForm, ImageUploadForm
from image_repository.models.user import UserManager
from utils.encrypt import Encryption

MAX_INT = 2 ** 31 - 1
MIN_INT = -2 ** 31


def index(request):
    return HttpResponseRedirect('login')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            user = UserManager.login_user(user_name, password)
            if user:
                encrypted_user_name = Encryption.encrypt(user_name).decode()
                return HttpResponseRedirect(reverse('image_repository:home', args=(encrypted_user_name,)))
    else:
        login_form = LoginForm()
    return render(request, 'image_repository/index.html', {
        'login_form': login_form,
    })


def home(request, encrypted_user_name):
    user_name = Encryption.decrypt(encrypted_user_name.encode())
    user = UserManager.get_user(user_name)
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST)
        if image_form.is_valid():
            print("VALID")
    else:
        image_form = ImageUploadForm()
    return render(request, 'image_repository/home.html', {
        'image_form': image_form,
        'url': encrypted_user_name,
        'first_name': user.first_name,
    })


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            data = signup_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            _ = UserManager.get_or_create_user(user_name, password, first_name, last_name)
            messages.success(request, 'Sign up successful')
            return HttpResponseRedirect(reverse('image_repository:login'))
    else:
        signup_form = SignUpForm()
    return render(request, 'image_repository/signup.html', {
        'signup_form': signup_form,
    })


def within_bounds(number) -> bool:
    if MIN_INT <= int(number) <= MAX_INT:
        return True
    return False
