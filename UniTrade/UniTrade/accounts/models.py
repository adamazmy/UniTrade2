                    ###   AUTHOR: ZIYAD ELGYZIRI   ###



from django.db import models

# Create your models here.

from  django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator


from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        # ... other fields if needed (e.g., first_name, last_name)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Password validators (adjust requirements as needed)
    validators = [
        MinLengthValidator(8),  # Minimum length of 8 characters
    ]

    def set_password(self, raw_password):
        super().set_password(raw_password)
        for validator in self.validators:
            validator(self.password)  # Validate password on save