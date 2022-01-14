from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# Create your views here.
from image_repository.models.user import User
from image_repository.models.image import Image

MAX_INT = 2 ** 31 - 1
MIN_INT = -2 ** 31


class IndexView(generic.ListView):
    template_name = 'image_repository/index.html'

    def get_queryset(self):
        return


class CreateUser(generic.CreateView):
    model = User
    template_name = 'image_repository/register.html'


class HomeView(generic.ListView):
    model = User, Image
    template_name = 'image_repository/home.html'

    def get_queryset(self):
        return Image.objects
