from django.db import models
from django.contrib.auth.models import User


class OneTimeCode(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_time = models.DateTimeField(auto_now_add=True)
