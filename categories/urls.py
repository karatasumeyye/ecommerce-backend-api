from django.urls import path

from products.views import admin_delete_product
from .views import *

urlpatterns = [
        
    path('', CatalogCategoryList.as_view(), name='catalog-category-list'),
    path('<int:pk>/', CatalogCategoryDetails.as_view(), name='catalog-category-details'),
    path('admin/',AdminCategoryList.as_view(), name='admin-category-list'),
    path('admin/<int:pk>/', AdminCategoryDetails.as_view(), name='admin-category-detail'),
    path('admin/create/', AdminCategoryCreate.as_view(), name='admin-create-category'),
    path('admin/<int:pk>/edit/', AdminCategoryEdit.as_view(), name='admin-edit-category'),
    path('admin/<int:pk>/delete/', AdminCategoryDelete.as_view(), name='admin-delete-category'),
]

