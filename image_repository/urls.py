from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'image_repository'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('register', views.register, name='register'),
    path('signin', views.home, name='signin'),
    path('home', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
