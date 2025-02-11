from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ShortenedURL
from django.http import HttpResponse

# Create your views here.

@csrf_exempt
def index(request):
    short_url = None
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            original_url = "https://" + original_url  # Ensure it's a valid URL

        short_url_obj = ShortenedURL.objects.create(original_url=original_url)
        short_url = f"https://sh-rtn.com/{short_url_obj.short_link}"
    return render(request, "index.html", {"short_url": short_url})

def MusicPage(request):
    return render(request, "Music.html")
def home(request):
    pages = [
        {"name": "Shorten URL", "url": "/shorten/"},
        {"name": "Music Converter", "url": "/music/"},
        {"name": "Home Page", "url": "/"},
    ]
    return render(request, 'home.html', {'pages': pages})

def redirect_url(request, short_link):
    url_entry = get_object_or_404(ShortenedURL, short_link=short_link)
    return redirect(url_entry.original_url)
