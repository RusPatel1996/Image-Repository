from typing import Optional, Any

from django.db import models


class UserManager(models.Manager):
    def get_or_create_user(self, username: str, password: str, first_name: Optional[str] = '',
                           last_name: Optional[str] = '') -> object:
        user, _ = self.get_or_create(
            user_name=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def update_or_create_user(self, user_id: int, username: str, password: str, first_name: Optional[str] = '',
                              last_name: Optional[str] = '') -> object:

        user, _ = self.update_or_create(
            user_name=username,
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
    user_name = models.CharField(unique=True, max_length=100, blank=False,
                                 help_text='Please add a user name less than 100 characters long')
    password = models.CharField(max_length=50, blank=False,
                                help_text='Please add a password less than 50 characters long')
    first_name = models.CharField(max_length=100, blank=True, null=True, default="Guest")
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_name

    objects = UserManager()
