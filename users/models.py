from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    # Custom user manager to handle user creation with email as username
    def create_user(self,email, password=None,**extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    # Create superuser method
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create(email,password,**extra_fields)
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Auto-generate username from email if not provided
    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = slugify(self.email.split('@')[0])
            username = base_username
            counter = 1

            while self.__class__.objects.filter(username=username).exists():
                username = f"{base_username}-{counter}"
                counter += 1

            self.username = username

        super().save(*args, **kwargs)