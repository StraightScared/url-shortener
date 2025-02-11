from django.shortcuts import render,get_object_or_404, redirect
from django.template import loader
import requests
import os

from django.views.decorators.csrf import csrf_exempt

from .models import ShortenedURL

from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def index(request):
    short_url = None
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        short_url_obj = ShortenedURL.objects.create(original_url=original_url)
        short_url = f"https://sh-rtn.com/{short_url_obj.short_link}"
    return render(request, "index.html", {"short_url": short_url})

def redirect_url(request, short_link):
    url_entry = get_object_or_404(ShortenedURL, short_link=short_link)
    return redirect(url_entry.original_url)
