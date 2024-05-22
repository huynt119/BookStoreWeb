from .models import *


def tags(request):
    return {'tags': Tag.objects.all()}

def latest_books(request):
    books = Book.objects.order_by('year')[:10]
    return {'latest_books': books}

def get_recommend_books(request):
    if not request.user.is_authenticated:
        books = Rating.get_top_rated_books(limit=10)
    else: 
        books_id = request.session["rec_books"]
        books = [Book.objects.get(item_id=book_id) for book_id in books_id]
    return {"rec_books": books}
