from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ShortenedURL
import random
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


def generate_board(rows=9, cols=9, mines=10):
    # Create an empty board as a list of lists (each cell is a dict).
    board = [[{'mine': False, 'adjacent': 0} for _ in range(cols)] for _ in range(rows)]

    # Randomly place mines on the board.
    positions = [(r, c) for r in range(rows) for c in range(cols)]
    mine_positions = random.sample(positions, mines)
    for r, c in mine_positions:
        board[r][c]['mine'] = True

    # Calculate adjacent mine counts for non-mine cells.
    for r in range(rows):
        for c in range(cols):
            if board[r][c]['mine']:
                continue
            count = 0
            for i in range(max(0, r - 1), min(rows, r + 2)):
                for j in range(max(0, c - 1), min(cols, c + 2)):
                    if board[i][j]['mine']:
                        count += 1
            board[r][c]['adjacent'] = count
    return board


def minesweeper(request):
    board = generate_board()
    return render(request, 'minesweeper/game.html', {'board': board})

def home(request):
    pages = [
        {"name": "Shorten URL", "url": "/shorten/"},
        {"name": "Minesweeper", "url": "/minesweeper/"},
        {"name": "Home Page", "url": "/"},
    ]
    return render(request, 'home.html', {'pages': pages})

def redirect_url(request, short_link):
    url_entry = get_object_or_404(ShortenedURL, short_link=short_link)
    return redirect(url_entry.original_url)
