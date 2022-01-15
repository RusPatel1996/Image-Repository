from typing import Optional

from django.db import models

from utils.encrypt import Encryption


class UserManager(models.Manager):
    def get_user(self, user_name: str) -> Optional[object]:
        user = None
        try:
            user = User.objects.get(user_name=user_name.lower())
        except User.DoesNotExist as err:
            print(f"User does not exist: {err}")
        except User.MultipleObjectsReturned as err:
            print(f"Multiple users found: {err}")
        return user

    def get_or_create_user(self, user_name: str, password: str, first_name: Optional[str] = '',
                           last_name: Optional[str] = '') -> object:
        user, _ = User.objects.get_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def update_or_create_user(self, user_id: int, user_name: str, password: str, first_name: Optional[str] = '',
                              last_name: Optional[str] = '') -> object:
        user, _ = User.objects.update_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def login_user(self, user_name: str, password: str) -> object:
        user = self.get_user(user_name)
        print(Encryption.decrypt(bytes(user.password, 'UTF-8')))
        print(Encryption.decrypt(password))
        if user and Encryption.decrypt(bytes(user.password, 'UTF-8')) == Encryption.decrypt(bytes(password, 'UTF-8')):
            return user
        return None

    def delete_user(self, user_name: str) -> Optional[tuple]:
        user = self.get_user(user_name)
        if user:
            return user.delete(user)
        return user


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(unique=True, max_length=100, blank=False)
    password = models.CharField(max_length=50, blank=False)

    objects = UserManager()

    def __str__(self):
        return self.user_name
