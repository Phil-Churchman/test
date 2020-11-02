from django.urls import path
from django.conf.urls import url
from .models import Category
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listingcreate", views.listingcreate, name="listingcreate"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:listing_id>", views.listingview, name="listingview"),
    path("<int:category_id>", views.index, name="index")
    
]
#     path("categories", views.category_view, name="categories"),

#     path("watchlist", views.watchlist, name="watchlist")
# ]
