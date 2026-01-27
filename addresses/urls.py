from django.urls import path
from .views import *

urlpatterns = [
    path('',AddressListView.as_view() , name='address-list'),
    path('create',AddressCreateView.as_view() , name='address-create'),
    path('<int:pk>',AddressDetailView.as_view(), name='address-detail'),
    path('<int:pk>/update', AddressUpdateView.as_view(), name='address-update'),
    path('<int:pk>/delete', AddressDeleteView.as_view(), name='address-delete'),
    path('admin',AdminAddressListView.as_view() , name='address-list'),
    path('admin/create',AdminAddressCreateView.as_view() , name='address-create'),
    path('admin/<int:pk>',AdminAddressDetailView.as_view(), name='address-detail'),
    path('admin/<int:pk>/update', AdminAddressUpdateView.as_view(), name='address-update'),
    path('admin/<int:pk>/delete', AdminAddressDeleteView.as_view(), name='address-delete'),
]   

# /
# admin/