from django.contrib import admin
from .models import Book, User, Tag, Rating, BookAdmin

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Rating)
