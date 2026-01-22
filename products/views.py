from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
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


@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
        products= Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer= ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def product_detail(request, pk):
        if request.method =='GET':
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method =='PUT':
             product = Product.objects.get(pk=pk)
             serializer=ProductSerializer(product,data=request.data)
             if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status= status.HTTP_200_OK)
             else: 
                  return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)