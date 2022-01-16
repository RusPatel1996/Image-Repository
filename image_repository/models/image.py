from PIL import Image as PILImage
from django.db import models
from django.utils.translation import gettext_lazy as _

from image_repository.models.user import User


class ImageManager(models.Manager):
    @staticmethod
    def search_image_characteristics(height: int, width: int, color: str):
        pass

    @staticmethod
    def search_image_by_text(name: str):
        pass

    @staticmethod
    def search_images_with_image(image):
        pass

    @staticmethod
    def get_user_images(user: User):
        return Image.objects.filter(user=user)

    @staticmethod
    def add_images(user: User, images, name=None):
        for image in images.getlist('image'):
            test = PILImage.open(image)
            print(test.format)
            print(test.size)
            print(test.getdata())
            Image.objects.create(user=user, name=(name if name else image), image=image)

    def calculate_color(self, image):
        pass


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    height = models.PositiveIntegerField(blank=False)
    width = models.PositiveIntegerField(blank=False)

    # class Color(models.TextChoices):
    #     RED = 'RED', _('Red')
    #     BLUE = 'BLU', _('Blue')
    #     GREEN = 'GRN', _('Green')
    #     WHITE = 'WHT', _('White')
    #     BLACK = 'BLK', _('Black')
    #
    # color = models.CharField(max_length=3, choices=Color.choices, blank=False)
    image = models.ImageField(upload_to='images/', height_field='height', width_field='width', blank=False,
                              help_text='Please add a image')

    # class Permission(models.IntegerChoices):
    #     PRIVATE = 0, _('Private')
    #     PUBLIC = 1, _('Public')
    #
    # permission = models.SmallIntegerField(choices=Permission.choices, blank=False, default=Permission.PRIVATE)
    last_updated = models.DateTimeField(auto_now_add=True, blank=False)

    objects = ImageManager()

    def __str__(self):
        return self.name
