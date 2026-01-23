from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from products.services import get_product_or_404
#
# def product_list(request):
#     products= Product.objects.all()
#     data = {
#         'products': list(products.values())
#     }
#     return JsonResponse(data)

# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#         data = {
#             'id': product.id,
#             'name': product.name,
#             'description': product.description,
#             'price': str(product.price),
#             'stock': product.stock,
#         }
#         return JsonResponse(data)
#     except Product.DoesNotExist:
#         return JsonResponse({'error': 'Product not found'}, status=404)


@api_view(["GET"])
def catalog_product_list(request):
    """Catalog: List all products"""
    if request.method == "GET":
        products = Product.objects.filter(
            stock__gt=0
        )  # Only products with stock greater than 0
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

@api_view(["GET"])
def catalog_list_product_by_catid(request,pk):
    """Catalog: List all products"""
    if request.method == "GET":
        products = Product.objects.filter(category=pk)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)



@api_view(["GET"])
def catalog_product_details(request, pk):
    """Catalog: Get product details"""
    product = get_product_or_404(pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_products(request):
    """Admin: List all products"""
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_product_details(request, pk):
    """Admin: Get product details"""
    product = get_product_or_404(pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def admin_create_product(request):
    """Admin: Create a new product"""
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def admin_edit_product(request, pk):
    """Admin: Edit an existing product"""
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def admin_delete_product(request, pk):
    """Admin: Delete a product"""
    product = get_product_or_404(pk)
    product.delete()
    return Response(
        {"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
