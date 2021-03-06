from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.conf import settings
class UserManager(BaseUserManager):
    """Creates custom user model"""
    def create_user(self, email, password = None, **extra_fields):
        """Creates and saves a new user in DB"""
        if not email:
            raise ValueError("Users must have an email address to sign in")
        user = self.model(email = self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using = self._db)


        return user

    def create_superuser(self,email,password):
        """Create and Save a new admin user"""

        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email instead of username"""
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField( max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Books(models.Model):
    book_id = models.CharField(max_length=255)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_return = models.BooleanField(default=False)
    is_borrowed = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.book_name