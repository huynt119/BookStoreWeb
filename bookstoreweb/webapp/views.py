from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Book
from .forms import SignInForm, SignUpForm
from django.template import loader

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def get_login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print("check post req")
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        print(form)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        return HttpResponseRedirect("/product/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignInForm()

    return render(request, "product.html", {"form": form})


def get_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/product/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()

    return render(request, "product.html", {"form": form})

def product(request):
    data = Book.objects.all()
    template = loader.get_template("product.html")
    context = {
        "books": data,
    }
    return HttpResponse(template.render(context, request))

def signin(request):
    return render(request, "signin.html")

