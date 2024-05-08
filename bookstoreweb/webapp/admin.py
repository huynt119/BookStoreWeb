from django.contrib import admin
from .models import Book, User, Tag, Rating, BookTag

# Register your models here.
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(BookTag)
admin.site.register(Rating)
