from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'image_repository'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('loout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('home/<str:user_name>/', views.home, name='home'),
    path('home/<str:user_name>/<str:image_hash>/', views.home, name='home'),
    path('home/<str:user_name>/<str:image_hash>/<str:image_name>/', views.view_image, name='view_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
