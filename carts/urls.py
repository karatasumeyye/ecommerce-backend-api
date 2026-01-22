from django.urls import path
from .views import *

urlpatterns = [
    path('',CartDetailView.as_view() , name='cart_detail'),
    path('add/',AddToCartView.as_view() , name='cart_add'),
    path('update/<int:pk>/',UpdateCartItemView.as_view() , name='cart_update'),
    path('delete/<int:pk>/',DeleteCartItemView.as_view() , name='cart_delete'),

    

    
]

# /
# admin/