from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import *

# Create your views here.
MAX_INT = 2**31-1
MIN_INT = -2**31


def index(request):
    return render(request, 'image_repository/index.html', {})\
