from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('developer', 'developer'),
        ('tester', 'tester'),
        ('manager', 'manager')
    ]
    id = models.UUIDField(default=uuid4, null=False, primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    role = models.CharField(choices=ROLES, max_length=10, null=False, default='developer')
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
