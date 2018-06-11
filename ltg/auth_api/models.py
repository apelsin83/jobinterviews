from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    token = models.CharField(blank=True, null=True, max_length=256)

    class Meta(object):
        unique_together = ('email',)

