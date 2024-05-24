from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# AdminClass
class BookAdmin(admin.ModelAdmin):
    filter_vertical = ('book_tags',)
    search_fields = ['title']

class RatingAdmin(admin.ModelAdmin):
    search_fields = ['rating']

class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

class UserAccountAdmin(UserAdmin):
    model = UserAccount

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
class BookQuantityAdmin(admin.ModelAdmin):
    search_fields = ['book__title']


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BookQuantity, BookQuantityAdmin)
