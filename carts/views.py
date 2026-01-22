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

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args,**kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)  # Fetch the product

        cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({"message": "Product added to cart successfully."}, status=status.HTTP_200_OK)
    

class CartDetailView(generics.RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
       cart, created = Cart.objects.get_or_create(user=self.request.user)   # Get or create cart for the user
       return cart
    

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request, pk):
        try:
           cart_item = CartItem.objects.get(pk=pk, cart__user = request.user)
        except CartItem.DoesNotExist:
            return NotFound("Cart item not found.")
        
        quantitiy = request.data.get('quantity')

        if quantitiy is None:
            return Response({"error": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if int(quantitiy) == 0:
            cart_item.delete()
            return Response({"message": "Cart item removed as quantity is set to zero."}, status=status.HTTP_200_OK)

        cart_item.quantity = quantitiy
        cart_item.save()
        return Response({"message": "Cart item updated successfully."}, status=status.HTTP_200_OK)
        
class DeleteCartItemView(APIView):
    permission_classes= [IsAuthenticated]

    def delete(self, request, pk):
        try:
           cart_item = CartItem.objects.get(pk=pk, cart__user = request.user)
        except CartItem.DoesNotExist:
            return NotFound("Cart item not found.")
        
        cart_item.delete()
        return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_200_OK)