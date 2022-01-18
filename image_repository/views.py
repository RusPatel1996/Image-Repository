from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from image_repository.forms import SignUpForm, LoginForm, ImageUploadForm, ImageSearchForm
from image_repository.models.image import ImageManager
from image_repository.models.user import UserManager
from utils.encrypt import Encryption

ImgMan = ImageManager.instance()  # Singleton
UsrMan = UserManager.instance()  # Singleton


def index(request):
    return redirect('image_repository:login')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            if user_id := UsrMan.login_user(user_name, password):
                request.session['user_name'] = user_name
                return redirect(reverse('image_repository:home', args=(user_name,)))
            else:
                messages.error(request, 'Wrong username or password')
    else:
        login_form = LoginForm()
    return render(request, 'image_repository/index.html', {
        'login_form': login_form,
    })


def logout(request):
    request.session.flush()
    return redirect('image_repository:login')


def home(request, user_name, image_hash=''):
    if request.session.get('user_name') != user_name:
        messages.error(request, 'Please login')
        return redirect(reverse('image_repository:login'))
    user = UsrMan.get_user(user_name)
    images = ImgMan.get_user_images(user)
    image_upload_form = ImageUploadForm()
    image_search_form = ImageSearchForm()
    if request.method == 'POST':
        if request.POST.get('action') == 'View':
            img = ImgMan.search_image_with_hash(user, image_hash)
            return render(request, 'image_repository/image.html', {
                'user_name': user_name,
                'image': img,
            })
        if request.POST.get('action') == 'Delete':
            ImgMan.delete_image(user, image_hash)
            messages.success(request, 'Deleted Successfully')
            return redirect(reverse('image_repository:home', args=(user_name,)))

        if request.POST.get('action') == 'Upload':
            count = images.count()
            upload(request, user)
            if images.count() > count:
                messages.success(request, 'Uploaded Successfully')
            else:
                messages.error(request, 'Upload Unsuccessful')
            return redirect(reverse('image_repository:home', args=(user_name,)))

        if request.POST.get('action') == 'Search':
            images = search(request, user)
            return home_render(request, image_upload_form, image_search_form, user_name, images)
    return home_render(request, image_upload_form, image_search_form, user_name, images)


def upload(request, user):
    image_upload_form = ImageUploadForm(request.POST, request.FILES)
    if image_upload_form.is_valid():
        data = image_upload_form.cleaned_data
        permission = data.get('permission')
        name = data.get('name')
        ImgMan.upload_images(user, request.FILES, permission, name)


def search(request, user):
    image_search_form = ImageSearchForm(request.POST, request.FILES)
    if image_search_form.is_valid():
        data = image_search_form.cleaned_data
        height = data.get('height')
        width = data.get('width')
        name = data.get('name')
        color = data.get('color')
        permission = data.get('permission')
        image = request.FILES.get('image')
        images = ImgMan.search_image_characteristics(user, color, permission, image, height, width, name)
        return images


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            data = signup_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            _ = UsrMan.get_or_create_user(user_name, password, first_name, last_name)
            messages.success(request, 'Sign up successful')
            return redirect(reverse('image_repository:login'))
    else:
        signup_form = SignUpForm()
    return render(request, 'image_repository/signup.html', {
        'signup_form': signup_form,
    })


def home_render(request, image_upload_form, image_search_form, user_name, images):
    return render(request, 'image_repository/home.html', {
        'image_upload_form': image_upload_form,
        'image_search_form': image_search_form,
        'user_name': user_name,
        'list_of_images': images
    })
