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
from rest_framework.exceptions import ValidationError
from core.utils import get_error_message


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        delivery_address_id = request.data.get("delivery_address_id")
        billing_address_id = request.data.get("billing_address_id")
        cart_data = request.data.get("cart_data")
        coupon_code = request.data.get("coupon_code")


        if not delivery_address_id or not billing_address_id:
            return Response(
                {
                    "error": "Both delivery_address_id and billing_address_id are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not cart_data:
            return Response(
                {"error": "cart_data is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_cart_or_create(request.user)

        try:
            order, payment_result = create_order_from_cart(
                request.user, cart, delivery_address_id, billing_address_id, cart_data, coupon_code
            )

        except ValidationError as e:
            return Response({"error": get_error_message(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred." + get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # =============================================
        # CELERY TASK ÇAĞRISI
        # =============================================
        # .delay() = görevi kuyruğa ekle, beklemeden devam et
        # Kullanıcı hemen yanıt alır, loglama arka planda yapılır
        log_new_order.delay(order.id)
        # =============================================

        return Response(
            {
                "message": "Order created successfully.",
                "order_id": order.id,
                "payment_result": payment_result,
            },
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
        return Order.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )  # Return orders for the logged-in user


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
