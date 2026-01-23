from .models import Category
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .services import get_category_or_404
class CatalogCategoryList(APIView):

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogCategoryDetails(APIView):
    def get(self,request, pk):
        category = get_category_or_404(pk)
        serializer = CaretegoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminCategoryList(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminCategoryDetails(APIView):
    permission_classes=[ IsAdminUser]
    def get(self,request, pk):
        category = get_category_or_404(pk)
        serializer = CaretegoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
       
class AdminCategoryCreate(APIView):

    permission_classes = [IsAdminUser]
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      


class AdminCategoryEdit(APIView):
    permission_classes = [IsAdminUser]

    def put(self,request, pk):
        category = get_category_or_404(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AdminCategoryDelete(APIView):
    permission_classes=[ IsAdminUser]
    def delete(self,request, pk):
        category = get_category_or_404(pk)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)