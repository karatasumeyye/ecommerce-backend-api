from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from products.models import Product
from rest_framework import generics
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.exceptions import NotFound
from products.services import get_product_or_404
from .services import (
    add_product_to_cart,
    get_cart_item_or_404,
    update_cart_item_quantity,
)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        add_product_to_cart(request.user, product_id, quantity)

        return Response(
            {"message": "Product added to cart successfully."},
            status=status.HTTP_200_OK,
        )


class CartDetailView(generics.RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )  # Get or create cart for the user
        return cart


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {"error": "Quantity must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item = get_cart_item_or_404(pk, request.user)
        updated_item = update_cart_item_quantity(cart_item, quantity)

        if updated_item is None:
            return Response(
                {"message": "Cart item removed as quantity was set to zero."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Cart item updated successfully."}, status=status.HTTP_200_OK
        )


class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return NotFound("Cart item not found.")

        cart_item.delete()
        return Response(
            {"message": "Cart item deleted successfully."}, status=status.HTTP_200_OK
        )
