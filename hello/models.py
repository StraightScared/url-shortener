import random
import string

from django.db import models

# Create your models here.


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

def generate_short_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenedURL(models.Model):
    short_link = models.CharField(max_length=20, unique=True, default=generate_short_link())
    original_url = models.URLField

    def __str__(self):
        return f"{self.short_link} -> {self.original_url}"
