from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=100, blank=False,
                                 help_text='Please add a user name less than 100 characters long')
    password = models.CharField(max_length=50, blank=False,
                                help_text='Please add a password less than 50 characters long')
    # email field would go here
    first_name = models.CharField(max_length=100, blank=True, null=True, default="Guest")
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user_name
