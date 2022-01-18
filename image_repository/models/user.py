from django.db import models


class UserManager(models.Manager):
    __instance = None

    @staticmethod
    def instance():
        if not UserManager.__instance:
            UserManager.__instance = UserManager()
            return UserManager.__instance
        return UserManager.__instance

    def get_user(self, user_name: str):
        try:
            user = User.objects.get(user_name=user_name.lower())
        except User.DoesNotExist as err:
            print(f"User does not exist: {err}")
        except User.MultipleObjectsReturned as err:
            print(f"Multiple users found: {err}")
        else:
            return user
        return None

    def get_or_create_user(self, user_name: str, password: bytes, first_name: str = '',
                           last_name: str = ''):
        user, _ = User.objects.get_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def update_or_create_user(self, user_name: str, password: bytes, first_name: str = '',
                              last_name: str = ''):
        user, _ = User.objects.update_or_create(
            user_name=user_name.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user

    def login_user(self, user_name: str, password: bytes):
        user = self.get_user(user_name)
        if user and user.password == password:
            return user.user_id
        return None

    def delete_user(self, user_name: str):
        user = self.get_user(user_name)
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
