from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("search/", views.search, name="search"),
    path("product/<slug:slug>/", views.product_detail, name="detail"),
    path("<str:gender>/<slug:slug>/", views.category_view, name="category"),
    path("<str:gender>/", views.gender_view, name="gender"),
]
