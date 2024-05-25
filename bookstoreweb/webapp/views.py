from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Book
from .forms import *
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from decimal import Decimal
from ml_model import *

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html', {})

def signin(request):
    if request.method == 'POST':
        if 'signin' in request.POST:
            signinform = AuthenticationForm(request, request.POST)
            signupform = SignUpForm()
            features = ["username", "password"]
            context = {
                'event' : 'signinForm',
                'signin_form' : signinform,
                'signup_form' : signupform
            }
            for key in features:
                if key in request.POST:
                    context[key] = request.POST[key]
            if signinform.is_valid():
                user = signinform.get_user()
                login(request, user)
                #get recommend books
                user_id = request.user.id
                books = recommend_books(user_id, 15)
                request.session["cart"] = []
                request.session["rec_books"] = books
                return redirect("/")
            else: 
                return render(request, 'signin.html', context)
        elif 'signup' in request.POST:
            signupform = SignUpForm(request.POST)
            signinform = AuthenticationForm()
            features = ["username", "password", "first_name", "last_name", "email", "phone_num", "password_repeat"]
            context = {
                'event' : 'signupForm',
                'signin_form' : signinform,
                'signup_form' : signupform
            }
            for key in features:
                if key in request.POST:
                    context[key] = request.POST[key]
            if signupform.is_valid():
            # Check if user exist on db
            # if not exist, save the user
            # redirect to a new URL:
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                # login(request, user)
                context['event'] = 'signinForm'
                return render(request, 'signin.html', context)
            else:
                return render(request, 'signin.html', context)
    else:
        return render(request, "signin.html")

def log_out(request):
    logout(request)
    return redirect("/")

RESULT_PER_PAGE = 18
DEFAULT_PAGE = 1
def get_page_range(request):
    try:
        page = max(int(request.GET.get('page', DEFAULT_PAGE)), DEFAULT_PAGE)
    except ValueError:
        page = DEFAULT_PAGE
    offset = (page - 1) * RESULT_PER_PAGE
    limit = offset + RESULT_PER_PAGE
    return offset, limit, page

def product(request):
    (offset, limit, page) = get_page_range(request)

    data = Book.objects.all()[offset:limit]
    template = loader.get_template("product.html")
    # latest_books = Book.objects.order_by('year')[:10]
    context = {
        "books": data,
        "id": offset,
        "next": page + 1,
        "prev": page - 1,
        # "latest_books": latest_books,
    }
    return HttpResponse(template.render(context, request))

def book_detail(request, item_id):
    book = get_object_or_404(Book, pk=item_id)
    ratings = Rating.get_ratings_of_book(book)
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, item_id=book.item_id).first()
    else: user_rating = 0
    avr_rate = book.get_avr_rating(ratings)
    tags = book.book_tags.all()
    context = {
            'book' : book,
            'ratings' : ratings,
            'avr_rate' : avr_rate,
            'tags': tags,
            'user_rating': user_rating
        }
    return render(request, 'bookdetail.html', context)

@login_required(login_url= "signin")
def userprofile(request):
    current_user = request.user
    transactions = Transaction.objects.filter(user=current_user)
    transaction_data = []
    
    for transaction in transactions:
        book_quantities = BookQuantity.objects.filter(transaction=transaction)
        transaction_data.append({
            'transaction': transaction,
            'book_quantities': book_quantities
        })
    form = UserUpdateForm(instance=request.user)

    context = {
        'user': current_user,
        'transaction': transaction_data,
        'form': form
    }
    return render(request, "user.html", context)

@login_required(login_url= "signin")
def add_to_cart(request, item_id):
    cart = request.session.get('cart', [])
    if item_id not in cart:
        cart.append(item_id)
    request.session['cart'] = cart
    messages.success(request, "Added successfully")
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url= "signin")
def payment(request):
    cart = request.session.get('cart', [])
    books = []
    for item_id in cart:
        book = get_object_or_404(Book, pk=item_id)
        books.append(book)
    # context['books'] = books
    context = {
        'books': books,
    }
    return render(request, 'payment.html', context)

@login_required(login_url= "signin")
# @require_http_methods(["POST"])
def purchase(request):
    total_amount = 0
    user = request.user  # Assumes the user is logged in
    card_number = request.POST.get('card_number')
    expiry_date = request.POST.get('expiry_date')
    cvv = request.POST.get('cvv')

    for key, value in request.POST.items():
        if key.startswith('book_'):
            book_id = int(key.split('_')[1])
            quantity = int(value)
            book = get_object_or_404(Book, pk=book_id)
            total_amount += book.price * quantity
            # Update session data or process as needed
            request.session['cart'][request.session['cart'].index(book_id)] = quantity
            
    total_amount = Decimal(total_amount)
    # Create a transaction
    transaction = Transaction(user=user, amount=total_amount)
    transaction.save()
    
    for key, value in request.POST.items():
        if key.startswith('book_'):
            book_id = int(key.split('_')[1])
            quantity = int(value)
            book = get_object_or_404(Book, pk=book_id)
            book_quantity = BookQuantity(transaction=transaction, book=book, quantity=quantity)
            book_quantity.save()
            
    # Clear cart data in session
    request.session['cart'] = []
    # Redirect to a new URL or render a success message
    return redirect('/')

@login_required(login_url= "signin")
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/userprofile/', request.user)  # Redirect to a profile page or some confirmation page
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'user.html', {'form': form})

def search_results(request):
    query = request.GET.get('q', '')
    (offset, limit, page) = get_page_range(request)
    data = Book.objects.filter(title__icontains=query)[offset:limit]
    template = loader.get_template("product.html")
    context = {
        "books": data,
        # "id": offset,
        "next": page + 1,
        "prev": page - 1,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url= "signin")
def delete_from_cart(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')
    cart = request.session.get('cart', [])
    del cart[request.session['cart'].index(int(item_id))]
    request.session['cart'] = cart
    return render(request, 'payment.html')

def tagged_books_view(request, tag):
    tag_obj = get_object_or_404(Tag, tag=tag)
    # return render(request, 'books_by_tag.html', {'books': books, 'tag': tag})
    try:
        page = max(int(request.GET.get('page', DEFAULT_PAGE)), DEFAULT_PAGE)
    except ValueError:
        page = DEFAULT_PAGE
    offset = (page - 1) * RESULT_PER_PAGE
    limit = offset + RESULT_PER_PAGE
    books = Book.objects.filter(book_tags=tag_obj.tag_id)[offset:limit]
    template = loader.get_template("product.html")
    context = {
        "books": books,
        "id": offset,
        "next": page + 1,
        "prev": page - 1,
        "tag": tag_obj
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url= "signin")
def rate_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('item_id')
        rating = request.POST.get('rating')
        user = request.user
        if user:
            # Update the user's rating for the book.
            # This assumes you have a model named UserRating with fields user, book, and rating.
            Rating.objects.update_or_create(user=user, item_id=book_id, defaults={'rating': rating})
            return render(request, 'homepage.html')
        else:
            return render(request, 'signin.html')
        


