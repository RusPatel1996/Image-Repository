from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from image_repository.forms import SignUpForm, LoginForm, ImageUploadForm, ImageSearchForm
from image_repository.models.image import ImageManager
from image_repository.models.user import UserManager
from utils.encrypt import Encryption


def index(request):
    return redirect('image_repository:login')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user_name = data.get('user_name')
            password = Encryption.encrypt(data.get('password'))
            if user_id := UserManager.login_user(user_name, password):
                request.session['user_id'] = user_id
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
    if not request.session.get('user_id'):
        messages.error(request, 'Please login')
        return redirect(reverse('image_repository:login'))
    User = UserManager.get_user(user_name)
    images = ImageManager.get_user_images(User)
    image_upload_form = ImageUploadForm()
    image_search_form = ImageSearchForm()
    if request.method == 'POST':
        if request.POST.get('action') == 'View':
            return redirect(reverse('image_repository:image', args=(user_name, image_hash,)))

        if request.POST.get('action') == 'Delete':
            ImageManager.delete_image(User, image_hash)
            messages.success(request, 'Deleted Successfully')
            return redirect(reverse('image_repository:home', args=(user_name,)))

        if request.POST.get('action') == 'Upload':
            upload(request, User)
            messages.success(request, 'Uploaded Successfully')
            return redirect(reverse('image_repository:home', args=(user_name,)))

        if request.POST.get('action') == 'Search':
            images = search(request)
            messages.success(request, f'Your Search Resulted {len(images)} Items')
            return home_render(request, image_upload_form, image_search_form, user_name, images)

    return home_render(request, image_upload_form, image_search_form, user_name, images)


def view_image(request, user_name, image_hash, image_name):
    img = ImageManager.search_image_with_hash(image_hash).image
    return render(request, 'image_repository/image.html', {
        'user_name': user_name,
        'image': img,
        'image_name': image_name
    })


def upload(request, User):
    image_upload_form = ImageUploadForm(request.POST, request.FILES)
    if image_upload_form.is_valid():
        data = image_upload_form.cleaned_data
        permission = data.get('permission')
        name = data.get('name')
        ImageManager.upload_images(User, request.FILES, permission, name)


def search(request):
    image_search_form = ImageSearchForm(request.POST, request.FILES)
    if image_search_form.is_valid():
        data = image_search_form.cleaned_data
        height = data.get('height')
        width = data.get('width')
        name = data.get('name')
        color = data.get('color')
        permission = data.get('permission')
        image = request.FILES.get('image')
        images = ImageManager.search_image_characteristics(color, permission, image, height, width, name)
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
            _ = UserManager.get_or_create_user(user_name, password, first_name, last_name)
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
