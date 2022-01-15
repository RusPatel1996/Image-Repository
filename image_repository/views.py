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


def register(request):
    return HttpResponseRedirect(reverse('image_repository:index'))


def home(request):
    return render(request, 'image_repository/home.html')


def index(request):
    return render(request, 'image_repository/index.html')


def signin(request):
    return HttpResponseRedirect(reverse('image_repository:home'))


def signup(request):
    return render(request, 'image_repository/signup.html')
