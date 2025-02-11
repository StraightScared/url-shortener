from django.shortcuts import render
from django.template import loader
import requests
import os

from django.views.decorators.csrf import csrf_exempt

from .models import Greeting
from .models import ShortenedURL

from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def index(request):
    short_url = None
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        short_url_obj = ShortenedURL.objects.create(original_url=original_url)
        short_url = f"https://sh.rtn.com/{short_url_obj.short_link}"
    return render(request, "index.html", {"short_url": short_url})


def db(request):
    # If you encounter errors visiting the `/db/` page on the example app, check that:
    #
    # When running the app on Heroku:
    #   1. You have added the Postgres database to your app.
    #   2. You have uncommented the `psycopg` dependency in `requirements.txt`, and the `release`
    #      process entry in `Procfile`, git committed your changes and re-deployed the app.
    #
    # When running the app locally:
    #   1. You have run `./manage.py migrate` to create the `hello_greeting` database table.

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
