from django.urls import path
from .views import *
urlpatterns=[
    path('',OrderListView.as_view(),name='create-list-order'),
    path('<int:pk>/',OrderDetailView.as_view(),name='order-detail'),
    path('create/', OrderCreateView.as_view(), name='create-order'),
    path('admin/',AdminOrderListView.as_view(),name='admin-order-list'),
    path('admin/<int:pk>/',AdminOrderDetailView.as_view(),name='admin-order-detail'),
    path('admin/<int:pk>/update-status/',AdminOrderStatusUpdateView.as_view(),name='admin-order-update'),
]