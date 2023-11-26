from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone


class BseUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'username'
    objects = auth_models.UserManager()

    username = models.CharField(max_length=20, unique=True, blank=False, null=False,)
    email = models.EmailField(unique=True, null=False, blank=False,)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(default=timezone.now)


class Profile(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=30,)
    last_name = models.CharField(blank=True, null=True, max_length=30,)
    user = models.OneToOneField(BseUser, on_delete=models.CASCADE, primary_key=True,)
