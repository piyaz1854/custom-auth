import bcrypt
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        if not password:
            raise ValueError("Password is required.")
        password_bytes = password.encode('utf-8') # use bytes
        salt = bcrypt.gensalt() # create some salt
        hashed_password = bcrypt.hashpw(password_bytes, salt) # hash with salt
        hashed_password_str = hashed_password.decode('utf-8') # use str
        user = self.model(
            email=email,
            password=hashed_password_str,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser must be with is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser must be with is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    #role:
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"] # for superuser
    objects = CustomUserManager() # use custom manager


    def __str__(self):
         return self.email

# Roles:
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    read_my_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    create_my_permission = models.BooleanField(default=False)
    create_all_permission = models.BooleanField(default=False)

    update_my_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)

    delete_my_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role.name} has access to: {self.element.name}, {self.element.id}"
