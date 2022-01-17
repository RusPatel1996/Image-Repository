from django.db import models

from utils.encrypt import Encryption


class UserManager(models.Manager):
    @staticmethod
    def get_user(user_name: str):
        try:
            user = User.objects.get(user_name=user_name.lower())
        except User.DoesNotExist as err:
            print(f"User does not exist: {err}")
        except User.MultipleObjectsReturned as err:
            print(f"Multiple users found: {err}")
        else:
            return user
        return None

    @staticmethod
    def get_or_create_user(user_name: str, password: bytes, first_name: str = '',
                           last_name: str = ''):
        user, _ = User.objects.get_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    @staticmethod
    def update_or_create_user(user_name: str, password: bytes, first_name: str = '',
                              last_name: str = ''):
        user, _ = User.objects.update_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    @staticmethod
    def login_user(user_name: str, password: bytes):
        user = UserManager.get_user(user_name)
        if user and Encryption.decrypt(user.password) == Encryption.decrypt(password):
            return user.user_id
        return None

    @staticmethod
    def delete_user(user_name: str):
        user = UserManager.get_user(user_name)
        if user:
            return user.delete(user)
        return user


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(unique=True, max_length=100, blank=False)
    password = models.BinaryField(max_length=50, blank=False)

    objects = UserManager()

    def __str__(self):
        return self.user_name
