from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICE = (
        ('admin', 'Admin'),
        ('user','User')
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='user')
    restricted = models.BooleanField(default=False)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email