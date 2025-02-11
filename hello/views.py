from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage
from django.template import loader
import requests
import tempfile
import os

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import ShortenedURL
from .music_separator.separator import MusicSeparator

separator = MusicSeparator()

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

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']

            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, uploaded_file.name)
            output_dir = os.path.join(temp_dir, 'output')

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            os.makedirs(output_dir, exist_ok=True)
            separator.separate_vocals(file_path, output_dir)

            output_file_path = os.path.join(output_dir, f"{os.path.splitext(uploaded_file.name)[0]}_vocals.wav")

            if os.path.exists(output_file_path):
                return FileResponse(open(output_file_path, 'rb'), content_type='audio/wav')
            else:
                return JsonResponse({'error': 'Processing failed.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

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
