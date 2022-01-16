from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from image_repository.forms import SignUpForm, LoginForm, ImageUploadForm, ImageSearchForm
from image_repository.models.user import UserManager
from image_repository.models.image import ImageManager
from utils.encrypt import Encryption


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
    images = ImageManager.get_user_images(user)
    if request.method == 'POST':
        image_upload_form = ImageUploadForm(request.POST, request.FILES)
        if image_upload_form.is_valid():
            data = image_upload_form.cleaned_data
            ImageManager.add_images(user, request.FILES, data.get('name'))
            messages.success(request, 'Added')
            return HttpResponseRedirect(reverse('image_repository:home', args=(encrypted_user_name,)))
    else:
        image_upload_form = ImageUploadForm()
        image_search_form = ImageSearchForm()
    return render(request, 'image_repository/home.html', {
        'image_upload_form': image_upload_form,
        'image_search_form': image_search_form,
        'url': encrypted_user_name,
        'first_name': user.first_name,
        'list_of_images': images
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