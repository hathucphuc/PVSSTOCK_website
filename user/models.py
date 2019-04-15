from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, email, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop(
            'is_superuser', False)
        user = self.model(
            email=email,
            is_active=True,
            is_provider=False,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, password=None,
            **extra_fields):
        return self._create_user(
            email, password, **extra_fields)

    def create_superuser(
            self, email, password,
            **extra_fields):
        return self._create_user(
            email, password,
            is_staff=True, is_superuser=True,
            **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField("staff status",default=False,help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField("active",default=True,help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_provider = models.BooleanField(default=False)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        if self.is_provider:
            return self.provider.name
        else:
            return self.email

class Provider(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	name = models.CharField(max_length=10,unique=True)
	full_name = models.CharField(max_length=100,unique=True)
	phone = models.CharField(max_length=15,unique=True)
	url = models.URLField(max_length=200,unique=True)
	slug = models.SlugField(max_length=30,unique=True)

	def __str__(self):
		return self.name
