from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'image_repository'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('home/<str:user_name>/', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
