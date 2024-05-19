from .models import Tag
from .models import Book

def tags(request):
    return {'tags': Tag.objects.all()}

def latest_books(request):
    books = Book.objects.order_by('year')[:10]
    print(books)
    return {'latest_books': books}