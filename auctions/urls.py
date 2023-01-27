from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),

    # 
    path("categories", views.category_view, name="category"),
    path("categories/<str:cate>", views.category_view, name="specific_category"),

    # NOT signed in
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    

    # User logged in
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("logout", views.logout_view, name="logout"),

    # listing pages
    path("listings/<str:id>", views.listing_view, name="specific_listing")

]
