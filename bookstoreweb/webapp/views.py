from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Book
from .forms import *
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html', {})

def get_login(request):
    # if this is a POST request we need to process the form data
    context = {
            "event": "signin"
        }
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        features = ["username", "password"]
        for field, errors in form.errors.items():
            pass
        context["errors"] = errors 
        for key in features:
            if key in request.POST:
                context[key] = request.POST[key]

        # create a form instance and populate it with data from the request:
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect("/product/")
        else:
            return render(request, "signin.html", context)
    else:
        form = AuthenticationForm(request)
        return render(request, "signin.html", context)
    # return HttpResponseRedirect("signin/")

def get_signup(request):
    context = {
        "event": "signup"
        }
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        features = ["username", "password", "first_name", "last_name", "email", "phone_num", "password_repeat"]
        for field, errors in form.errors.items():
            pass
        context["errors"] = errors 
        for key in features:
            if key in request.POST:
                context[key] = request.POST[key]
        if form.is_valid():
            print("signup valid")
            # Check if user exist on db
            # if not exist, save the user
            # redirect to a new URL:
            form.save()
            context["event"] = "signin"
            return render(request, "signin.html", context)
        else:
            print("invalid form")
            return render(request, "signin.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request, "signin.html", context)
    

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
                request.session["cart"] = []
                return redirect("/product/")
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
            print(signupform.errors)
            if signupform.is_valid():
                print("valid")
            # Check if user exist on db
            # if not exist, save the user
            # redirect to a new URL:
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("/product/")
            else:
                print("invalid")
                return render(request, 'signin.html', context)
    else:
        return render(request, "signin.html")

def log_out(request):
    logout(request)
    return render(request, 'homepage.html')

RESULT_PER_PAGE = 18
def product(request):
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * RESULT_PER_PAGE
    limit = offset + RESULT_PER_PAGE

    data = Book.objects.all()[offset:limit]
    template = loader.get_template("product.html")
    context = {
        "books": data,
        "id": offset,
        "next": page + 1,
        "prev": page - 1,
    }
    return HttpResponse(template.render(context, request))

def book_detail(request, item_id):
    book = get_object_or_404(Book, pk=item_id)
    ratings = Rating.get_ratings_of_book(book)
    avr_rate = book.get_avr_rating(ratings)
    context = {
            'book' : book,
            'ratings' : ratings,
            'avr_rate' : avr_rate
        }
    return render(request, 'bookdetail.html', context)

@login_required(login_url= "signin")
def userprofile(request):
    current_user = request.user
    return render(request, "user.html", {'user' : current_user})

@login_required(login_url= "signin")
def add_to_cart(request, item_id):
    # print("fuck")
    # book = get_object_or_404(Book, pk=item_id)
    # book_id = book.item_id
    # if book_id:
    # print("session data: ", request.session['cart'])
    cart = request.session.get('cart', [])
    cart.append(item_id)
    request.session['cart'] = cart
    print("cart: ", request.session['cart'])
    return render(request, 'homepage.html')

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



