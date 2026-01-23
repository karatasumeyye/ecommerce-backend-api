from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer, OrderStatusUpdateSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response(
                {"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(user=user)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

        order.calculate_total()
        cart.items.all().delete()  # Clear the cart after creating the order
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

    