from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_manager = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.username