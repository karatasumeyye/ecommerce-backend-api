from django.urls import path
from .views import *

urlpatterns = [
    path('', catalog_product_list, name='catalog-list-products'),
    path('<int:pk>/', catalog_product_details, name='catalog-product-detail'),
    path('category/<int:pk>/', catalog_list_product_by_catid, name='catalog-list-products-by-catid'),
    path('admin/',admin_list_products, name='admin-list-products'),
    path('admin/<int:pk>/', admin_product_details, name='admin-product-detail'),
    path('admin/create/', admin_create_product, name='admin-create-product'),
    path('admin/<int:pk>/edit/', admin_edit_product, name='admin-edit-product'),
    path('admin/<int:pk>/delete/', admin_delete_product, name='admin-delete-product'),
]

# /
# admin/