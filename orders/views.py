from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from django.db import transaction
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from .tasks import log_new_order  # ← Celery task'ını import et


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        user = request.user
        cart = get_cart_or_create(request.user)
        order = create_order_from_cart(request.user,cart)
        
        # =============================================
        # CELERY TASK ÇAĞRISI
        # =============================================
        # .delay() = görevi kuyruğa ekle, beklemeden devam et
        # Kullanıcı hemen yanıt alır, loglama arka planda yapılır
        log_new_order.delay(order.id)
        # =============================================
       
        return Response(
            {"message": "Order created successfully.", "order_id": order.id},
            status=status.HTTP_201_CREATED,
        )


class OrderListView(generics.ListAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )  # Return orders for the logged-in user

class OrderDetailView(generics.RetrieveAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_by('-created_at')  # Return orders for the logged-in user
    

class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.order_by("-created_at")


class AdminOrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    