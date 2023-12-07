from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


class User(AbstractUser):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.username





    


