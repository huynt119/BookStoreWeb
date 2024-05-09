from django.db import models
from django.contrib import admin

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=100)
    tag_id = models.AutoField(primary_key=True, unique=True)

    def __str__(self):
        return self.tag

class Book(models.Model):
    item_id = models.AutoField(primary_key=True, unique=True)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    lang = models.CharField(max_length=50)
    img = models.URLField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book_tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Rating(models.Model):
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rating_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_user')
    rating = models.IntegerField()

    def __str__(self):
        return str(self.user) + ' rating: ' + str(self.item)
    




# AdminClass
class BookAdmin(admin.ModelAdmin):
    filter_vertical = ('book_tags',)