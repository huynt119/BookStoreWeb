from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
import json
from .views import *
from django.contrib.sessions.backends.db import SessionStore
from .forms import UserUpdateForm

# TEST CASE MODELS
class BookModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            item_id=1,
            url="product/1/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )

    def test_str(self):
        book = self.book
        self.assertEqual(str(book), 'Test Book')

    def test_get_avr_rating(self):
        book = self.book
        user = self.user
        Rating.objects.create(item=book, user=user, rating=5)
        Rating.objects.create(item=book, user=user, rating=3)
        ratings = book.rating_item.all()
        self.assertEqual(book.get_avr_rating(ratings), 4.0)

class UserAccountModelTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            username='testuser', 
            first_name='John', 
            last_name='Doe', 
            phone_num='1234567890'
        )
    def test_str(self):
        user = self.user
        self.assertEqual(str(user), 'John Doe')

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(tag='Fiction')
    def test_str(self):
        tag = self.tag
        self.assertEqual(str(tag), 'Fiction')

class RatingModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book1 = Book.objects.create(
            item_id=1,
            url="product/1/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
        self.book2 = Book.objects.create(
            item_id=2,
            url="product/2/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
    def test_str(self):
        book = self.book1
        user = self.user
        rating = Rating.objects.create(item=book, user=user, rating=5)
        self.assertEqual(str(rating), 'Test User rating: Test Book')
    
    def test_get_ratings_of_book(self):
        book = self.book1
        user = self.user
        rating = Rating.objects.create(item=book, user=user, rating=5)
        ratings = Rating.get_ratings_of_book(book)
        self.assertIn(rating, ratings)
    
    def test_get_top_rated_books(self):
        tag = Tag.objects.create(tag='Fiction')
        book1 = self.book1
        book2 = self.book2
        book1.book_tags.add(tag)
        book2.book_tags.add(tag)
        user = self.user
        Rating.objects.create(item=book1, user=user, rating=5)
        Rating.objects.create(item=book2, user=user, rating=4)
        top_books = Rating.get_top_rated_books()
        self.assertIn(book1, top_books)
        self.assertIn(book2, top_books)

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.book = Book.objects.create(
            item_id=1,
            url="product/1/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
    def test_str(self):
        user = self.user
        transaction = Transaction.objects.create(user=user, amount=100.0)
        self.assertEqual(str(transaction), 'Test User purchased ')

class BookQuantityModelTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.book = Book.objects.create(
            item_id=1,
            url="product/1/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
    def test_str(self):
        user = self.user
        transaction = Transaction.objects.create(user=user, amount=100.0)
        book = self.book
        book_quantity = BookQuantity.objects.create(transaction=transaction, book=book, quantity=3)
        self.assertEqual(str(book_quantity), 'Test Book - Quantity: 3')

# TEST CASE VIEWS
class HomepageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home') 
    def test_homepage_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  
    def test_homepage_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'homepage.html') 
    def test_homepage_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Welcome to our Book Store!')  

class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.signin_url = reverse('signin')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

    def test_signin_get(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_signin_post_valid(self):
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'password', 'signin': ''})
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signin_post_invalid(self):
        response = self.client.post(self.signin_url, {'username': 'testuser', 'password': 'wrongpassword', 'signin': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_signup_post_valid(self):
        response = self.client.post(self.signin_url, {
            'username': 'newuser',
            'password': 'newpassword',
            'password_repeat': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone_num': '1234567890',
            'signup': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'signinForm')
        new_user = UserAccount.objects.filter(username='newuser').exists()
        self.assertTrue(new_user)

    def test_signup_post_invalid(self):
        response = self.client.post(self.signin_url, {
            'username': 'newuser',
            'password': 'newpassword',
            'password_repeat': 'mismatch',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone_num': '1234567890',
            'signup': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'signupForm')
        new_user = UserAccount.objects.filter(username='newuser').exists()
        self.assertFalse(new_user)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserAccount.objects.create_user(
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.tag = Tag.objects.create(tag='Fiction')
        self.book = Book.objects.create(
            item_id=5,
            url="product/5/",
            title="Test Book",
            authors="Author",
            lang="en",
            img="http://example.com/image.jpg",
            year=2022,
            description="This is a test book",
            price=9.99
        )
        self.book.book_tags.add(self.tag)
        self.transaction = Transaction.objects.create(user=self.user, amount=100)
        self.book_quantity = BookQuantity.objects.create(transaction=self.transaction, book=self.book, quantity=1)
        self.factory = RequestFactory()
        self.client.login(username='testuser', password='password123')
        session = SessionStore()
        
        # Gán session cho client
        self.client.cookies['sessionid'] = session.session_key


    def test_remove_cart(self):
        session = self.client.session
        cart = session.get('cart', [])
        cart.append(self.book.item_id)
        session['cart'] = cart
        session.save()
        response = self.client.post(reverse('delete_from_cart'), data=json.dumps({'item_id': self.book.item_id}), content_type='application/json')
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart = session.get('cart', [])
        # Kiểm tra xem sản phẩm đã bị xóa khỏi giỏ hàng
        self.assertNotIn(self.book.item_id, cart)

    def test_tagged_books_view(self):
        response = self.client.get(reverse('tagged_books', args=[self.tag.tag]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_rate_book(self):   
        response = self.client.post(reverse('book_detail', args=[self.book.item_id]))  
        response = self.client.post(reverse('rate_book'))
        Rating.objects.create(item=self.book, user=self.user, rating=5)
        self.assertEqual(response.status_code, 302)
        rating = Rating.objects.get(item=self.book, user=self.user)
        self.assertEqual(rating.rating, 5)
        
    def test_get_page_range(self):
        request = self.factory.get('/?page=2')
        offset, limit, page = get_page_range(request)
        self.assertEqual(offset, 18)
        self.assertEqual(limit, 36)
        self.assertEqual(page, 2)

    def test_product_view(self):
        response = self.client.get(reverse('product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book.item_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookdetail.html')
        self.assertContains(response, self.book.title)

    def test_userprofile_view(self):
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'testuser')

    def test_add_to_cart_view(self):
        session = self.client.session
        cart = session.get('cart', [])
        cart.append(self.book.item_id)
        response = self.client.get(reverse('add_to_cart', args=[self.book.item_id]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart = session.get('cart', [])
        self.assertNotIn(self.book.item_id, cart)

    def test_payment_view(self):
        session = self.client.session
        cart = session.get('cart', [])
        cart.append(self.book.item_id)
        session.save()
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 302)

    def test_purchase_view(self):
        session = self.client.session
        cart = session.get('cart', [])
        cart.append(self.book.item_id)
        session.save()
        response = self.client.post(reverse('purchase'), {
            'card_number': '1234567890123456',
            'expiry_date': '12/25',
            'cvv': '123',
            'book_{}'.format(self.book.item_id): 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1) 
        session = self.client.session
        cart = session.get('cart', [])
        # Kiểm tra xem sản phẩm đã bị xóa khỏi giỏ hàng
        self.assertNotIn(self.book.item_id, cart)

    def test_update_profile_view(self):
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('update_profile'), {
            'username': 'testuser_updated',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser_updated')

    def test_search_results_view(self):
        response = self.client.get(reverse('search_results'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertContains(response, self.book.title)

