from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
    
class UserAccount(AbstractUser):
    phone_num = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
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
    
    def get_avr_rating(self, ratings):
        total = 0
        for rate in ratings:
            total += rate.rating
        num = len(ratings)
        if num == 0:
            return 0
        return round(total / num, 2)
    
class Rating(models.Model):
    item = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='rating_item')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='rating_user')
    rating = models.IntegerField()

    def __str__(self):
        return str(self.user) + ' rating: ' + str(self.item)
    
    def get_ratings_of_book(item):
        ratings = Rating.objects.filter(item = item)
        return ratings
    
    # Get 10 books have highest ovr rate score
    def get_top_rated_books(limit=10):
        top_books = (
            Book.objects.annotate(num_ratings=Count('rating_item'))
            .order_by('-num_ratings')[:10]
        )
        return top_books

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.user) + ' purchased '

class BookQuantity(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='book_quantity')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quantity')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.book) + ' - Quantity: ' + str(self.quantity)

