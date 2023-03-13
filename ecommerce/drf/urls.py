from django.urls import path

from . import views 

urlpatterns = [
    path("categories", views.CategoryListView.as_view(), name="category-list"),
    path("categories/<slug:slug>", views.CategoryRetrieveView.as_view(), name="category-detail"),
    path("categories/<slug:slug>/products", views.CategoryProductListView.as_view(), name="category-product-list"),
    path("categories/<slug:slug>/products/<int:web_id>", views.ProductRetrieveView.as_view(), name="category-product-detail"),
    path("products", views.ProductListView.as_view(), name="product-list"),
    path("products/<int:web_id>", views.ProductRetrieveView.as_view(), name="product-detail"),
    path("inventory", views.ProductInventoryListView.as_view(), name="inventory-list"),
    path("inventory/<sku>", views.ProductInventoryRetrieveView.as_view(), name="inventory-detail"),
]