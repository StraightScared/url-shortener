import random
import string
from django.apps import apps
from django.db import models

# Create your models here.


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

def generate_short_link():
    ShortenedURL = apps.get_model('hello', 'ShortenedURL')
    while True:
        short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not ShortenedURL.objects.filter(short_link=short_link).exists():
            return short_link

class ShortenedURL(models.Model):
    short_link = models.CharField(max_length=20, unique=True, default=generate_short_link)
    original_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.short_link} -> {self.original_url}"
