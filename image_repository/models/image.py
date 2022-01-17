import sys
from io import BytesIO
from math import ceil

import PIL.Image
import imagehash
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from sklearn.cluster import KMeans

from image_repository.models.user import User


class ImageManager(models.Manager):
    @staticmethod
    def search_image_characteristics(color, permission, image=None, height=None, width=None, name=''):
        height = 0 if not height else height
        width = 0 if not width else width
        objects = Image.objects.filter(height__gte=height, width__gte=width, name__icontains=name)
        if color != Image.Color.ANY:
            objects = objects.filter(color__exact=color)
        if permission != Image.Permission.ALL:
            objects = objects.filter(permission__exact=permission)
        if image:
            objects = ImageManager.search_images_with_image(image, objects, similarity=75)
        return objects

    @staticmethod
    def search_images_with_image(image, objects, similarity):
        threshold = 1 - (similarity / 100)
        diff_limit = int(threshold * (8 ** 2))  # 8 refers to the default hash size for dhash
        image_hash = ImageManager.get_image_hash(image)
        for obj in objects:
            if abs(image_hash - imagehash.hex_to_hash(obj.image_hash)) <= diff_limit:
                yield obj

    @staticmethod
    def search_image_with_hash(image_hash):
        return Image.objects.filter(image_hash__exact=image_hash).first()

    @staticmethod
    def get_image_hash(image):
        pil_image = PILImage.open(image)
        return imagehash.dhash(pil_image)

    @staticmethod
    def get_user_images(user: User):
        return Image.objects.filter(user__exact=user)

    @staticmethod
    def upload_images(user: User, images, permission, name=''):
        """ Can upload large amounts of images quickly by reducing them to 150px or less and optimizing before saving
        to database. Remove color field to increase performance. Images are uploaded as private unless otherwise
        chosen by the user. """
        for image in images.getlist('image'):
            img = ImageManager.resize_image(image, 750)
            thumbnail = ImageManager.resize_image(image, 150)
            img_hash = imagehash.dhash(img)
            if image_object := ImageManager.search_image_with_hash(img_hash):
                name = name if name else image_object.name
                color = image_object.color
                thumbnail = image_object.thumbnail
                img = image_object.image
            else:
                name = name if name else image.name.split('.')[0]
                color = ImageManager.get_color(thumbnail)
                thumbnail = ImageManager.convert_image_back_from_pillow(thumbnail, name)

                # Even though we're optimizing the image in within the following function, image hash remains the
                # same for higher quality values
                img = ImageManager.convert_image_back_from_pillow(img, name)

            Image.objects.create(user=user, name=name, image=img, thumbnail=thumbnail, image_hash=img_hash, color=color,
                                 permission=permission)

    @staticmethod
    def get_color(image):
        red, green, blue = ImageManager.calculate_rgb(image)
        primary_threshold = 0.85
        secondary_threshold = 0.50
        if red / (green + blue) > primary_threshold:
            return Image.Color.RED
        elif green / (red + blue) > primary_threshold:
            return Image.Color.GREEN
        elif blue / (red + green) > primary_threshold:
            return Image.Color.BLUE
        else:
            majority = max(red, green, blue)
            if majority == red:
                if red / (green + blue) > secondary_threshold:
                    return Image.Color.YELLOW
                return Image.Color.RED
            elif majority == green:
                if green / (red + blue) > secondary_threshold:
                    return Image.Color.CYAN
                return Image.Color.GREEN
            else:
                if blue / (red + green) > secondary_threshold:
                    return Image.Color.PURPLE
                return Image.Color.BLUE

    @staticmethod
    def convert_image_back_from_pillow(image, name):
        output = BytesIO()
        image.save(output, format='JPEG', quality=95, optimize=True)
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', f"{name}.jpg", 'image/jpeg',
                                    sys.getsizeof(output), None)

    @staticmethod
    def calculate_rgb(image):
        """ Slows down the uploading performance by at least 4x """
        pixels = image.getdata()
        n = 2
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_
        red, green, blue = 0, 0, 0
        for rgb in centers:
            red += rgb[0]
            green += rgb[1]
            blue += rgb[2]
        red, green, blue = red // n, green // n, blue // n

        return red, green, blue

    @staticmethod
    def resize_image(image, largest_length):
        pil_image = PILImage.open(image)
        pil_image = pil_image.convert('RGB')
        width, height = pil_image.size
        factor = width / largest_length if width > height else height / largest_length
        width, height = ceil(width / factor), ceil(height / factor)
        return pil_image.resize((width, height), PIL.Image.HAMMING, None, 1.5)

    @staticmethod
    def delete_image(user: User, image):
        Image.objects.get(user=user, image=image)


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    height = models.PositiveIntegerField(blank=False)
    width = models.PositiveIntegerField(blank=False)
    image = models.ImageField(upload_to='images/', height_field='height', width_field='width', blank=False)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=False)
    image_hash = models.CharField(max_length=50, blank=False)

    class Color(models.TextChoices):
        ANY = 'Any',
        RED = 'Red',
        BLUE = 'Blue',
        GREEN = 'Green',
        YELLOW = 'Yellow',
        PURPLE = 'Purple'
        CYAN = 'Cyan'

    color = models.CharField(max_length=7, choices=Color.choices, default=Color.ANY)

    class Permission(models.TextChoices):
        ALL = 'All',
        PRIVATE = 'Private',
        PUBLIC = 'Public',

    permission = models.CharField(max_length=7, choices=Permission.choices, blank=False, default=Permission.ALL)
    last_updated = models.DateTimeField(auto_now_add=True, blank=False)

    objects = ImageManager()

    def __str__(self):
        return self.name
