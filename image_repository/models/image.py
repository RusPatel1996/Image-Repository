import sys
from io import BytesIO
from math import ceil

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from image_repository.models.user import User
from PIL import Image as PILImage
import imagehash

from sklearn.cluster import KMeans


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
    def search_images_with_image(image):
        # TODO: add the rest of the functionality

        image_hash = imagehash.average_hash(PILImage.open(image))
        ImageManager.search_image_with_hash(image_hash)
        pass

    @staticmethod
    def search_image_with_hash(image_hash):
        return Image.objects.filter(image_hash__exact=image_hash).first()

    @staticmethod
    def get_user_images(user: User):
        return Image.objects.filter(user=user)

    @staticmethod
    def add_images(user: User, images, permission, name=''):
        for image in images.getlist('image'):
            image = ImageManager.resize_image(image, 150)
            image_hash = imagehash.average_hash(image)
            if image_object := ImageManager.search_image_with_hash(image_hash):
                name = name if name else image_object.name
                image = image_object.image
                color = image_object.color
            else:
                # TODO fix name
                name = name if name else "test"
                color = ImageManager.calculate_color(image)
                image = ImageManager.compress_size(image, name)
            Image.objects.create(user=user, name=name, image=image, image_hash=image_hash, color=color,
                                 permission=permission)

    @staticmethod
    def compress_size(img, name):
        output = BytesIO()
        img.save(output, format='JPEG', quality=95)
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % name, 'image/jpeg',
                                    sys.getsizeof(output), None)

    @staticmethod
    def calculate_color(img):
        ''' Slows down the uploading performance by at least 4x '''
        pixels = img.getdata()
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

        return ImageManager.get_color(red, green, blue)

    @staticmethod
    def get_color(red, green, blue):
        primary_rate = 0.85
        secondary_rate = 0.50
        if red / (green + blue) > primary_rate:
            return Image.Color.RED
        elif green / (red + blue) > primary_rate:
            return Image.Color.GREEN
        elif blue / (red + green) > primary_rate:
            return Image.Color.BLUE
        else:
            majority = max(red, green, blue)
            if majority == red:
                if red / (green + blue) > secondary_rate:
                    return Image.Color.YELLOW
                return Image.Color.RED
            elif majority == green:
                if green / (red + blue) > secondary_rate:
                    return Image.Color.CYAN
                return Image.Color.GREEN
            else:
                if blue / (red + green) > secondary_rate:
                    return Image.Color.PURPLE
                return Image.Color.BLUE


    @staticmethod
    def resize_image(image, largest_length):
        pil_image = PILImage.open(image)
        pil_image = pil_image.convert('RGB')
        width, height = pil_image.size
        factor = width / largest_length if width > height else height / largest_length
        width, height = ceil(width / factor), ceil(height / factor)
        return pil_image.resize((width, height))

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
    image_hash = models.CharField(max_length=50, blank=False)

    class Color(models.TextChoices):
        ANY = 'Any',
        RED = 'Red',
        BLUE = 'Blue',
        GREEN = 'Green',
        YELLOW = 'Yellow',
        PURPLE = 'Purple'
        CYAN = 'Cyan'

    color = models.CharField(max_length=7, choices=Color.choices, blank=True, default=Color.ANY)

    class Permission(models.TextChoices):
        ALL = 'All',
        PRIVATE = 'Private',
        PUBLIC = 'Public',

    permission = models.CharField(max_length=7, choices=Permission.choices, blank=False, default=Permission.ALL)
    last_updated = models.DateTimeField(auto_now_add=True, blank=False)

    objects = ImageManager()

    def __str__(self):
        return self.name
