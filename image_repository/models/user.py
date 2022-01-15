from typing import Optional, Any

from django.db import models
from collections import defaultdict


class UserManager(models.Manager):
    def get_or_create_user(self, user_name: str, password: str, first_name: Optional[str] = '',
                           last_name: Optional[str] = '') -> object:
        user, _ = self.get_or_create(
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def update_or_create_user(self, user_id: int, user_name: str, password: str, first_name: Optional[str] = '',
                              last_name: Optional[str] = '') -> object:

        user, _ = self.update_or_create(
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def delete_user(self, user_id: int) -> tuple:
        user = None
        try:
            user = self.objects.get(id=user_id)
        except self.DoesNotExist as err:
            print(f"User does not exist: {err}")
        except self.MultipleObjectsReturned as err:
            print(f"Multiple users found: {err}")
        else:
            return user.delete()
        return ()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(unique=True, max_length=100, blank=False)
    password = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.user_name

    objects = UserManager()
