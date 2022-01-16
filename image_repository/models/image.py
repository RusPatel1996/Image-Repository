import sys
from io import BytesIO
from math import ceil

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from Shopify_Data_Engineer_Intern_Challenge_Summer_2022.settings import MEDIA_URL, MEDIA_ROOT
from image_repository.models.user import User

from cv2 import imread
from numpy import average
from PIL import Image as Pimg


class ImageManager(models.Manager):
    @staticmethod
    def search_image_characteristics(color, permission, height=0, width=0, name=''):
        objects = Image.objects.filter(height__gt=height, width__gt=width, name__icontains=name)
        if color != Image.Color.ANY:
            objects = objects.filter(color=color)
        if permission != Image.Permission.ALL:
            objects = objects.filter(permission=permission)
        return objects

    @staticmethod
    def get_user_images(user: User):
        return Image.objects.filter(user=user)

    @staticmethod
    def add_images(user: User, images, permission, name=''):
        for image in images.getlist('image'):
            if not name:
                name = image.name.split('.')[0]
            image = ImageManager.compress_size(image, name)
            Image.objects.create(user=user, name=name, image=image, permission=permission)

    @staticmethod
    def compress_size(image, name):
        img = Pimg.open(image)
        output = BytesIO()
        width, height = img.size
        factor = ceil(width / 200) if width > height else ceil(height / 200)
        img = img.resize((width // factor, height // factor))
        img.save(output, format='JPEG', quality=95)
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % name, 'image/jpeg',
                                   sys.getsizeof(output), None)

    @staticmethod
    def delete_image(user: User, image):
        Image.objects.get(user=user, image=image)

    @staticmethod
    def search_images_with_image(image):
        pass

    @staticmethod
    def calculate_color(image):
        pass


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    height = models.PositiveIntegerField(blank=False)
    width = models.PositiveIntegerField(blank=False)
    image = models.ImageField(upload_to='images/', height_field='height', width_field='width', blank=False,
                              help_text='Please add a image')

    class Color(models.TextChoices):
        ANY = 'Any',
        RED = 'Red',
        BLUE = 'Blue',
        GREEN = 'Green',
        WHITE = 'White',
        BLACK = 'Black',

    color = models.CharField(max_length=7, choices=Color.choices, blank=False, default=Color.ANY)

    class Permission(models.TextChoices):
        ALL = 'All',
        PRIVATE = 'Private',
        PUBLIC = 'Public',

    permission = models.CharField(max_length=7, choices=Permission.choices, blank=False, default=Permission.ALL)
    last_updated = models.DateTimeField(auto_now_add=True, blank=False)

    objects = ImageManager()

    def __str__(self):
        return self.name
