"""
URL configuration for bookstoreweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.homepage, name = 'test'),
    path('product/', views.product, name='product'),
    path('signin/', views.signin, name='signin'),
    path('product/<int:item_id>', views.book_detail, name='book_detail'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('logout/', views.log_out ,name='logout'),
    path('add/<int:item_id>', views.add_to_cart, name="add_to_cart"),
    path('payment/', views.payment, name="payment"),
    path('purchase/', views.purchase, name='purchase'),
    path('userprofile/update/', views.update_profile, name='update_profile'),
    # path('product/<int:book_id>/rate/', views.submit_rating, name='submit_rating'),
    path('product/search/', views.search_results, name='search_results'),
    path('cart/delete', views.delete_from_cart, name='delete_from_cart'),
    path('product/<str:tag>/', views.tagged_books_view, name='tagged_books'),
    path('rate_book/', views.rate_book, name='rate_book'),
]
