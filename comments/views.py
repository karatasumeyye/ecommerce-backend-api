from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from comments.filters import CommentFilter

from .models import Comment
from .serializers import CommentSerializer
from rest_framework.exceptions import ValidationError,PermissionDenied
from core.paginations import StandardResultsSetPagination, LargeResultsSetPagination

class AdminCommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LargeResultsSetPagination
    queryset= Comment.objects.all().order_by('-update')
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    # def get_queryset(self):
    #    pk= self.kwargs.get('pk')   # product id
    #    queryset = Comment.objects.all()

    #    if pk:
    #        queryset= Comment.objects.filter(product_id=pk)
    #    return queryset.order_by('-update')


class AdminCommentEdit(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


class AdminCommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]



class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
       pk= self.kwargs['pk']
       return Comment.objects.filter(product_id=pk)

class CommentCreate(generics.CreateAPIView):
    serializer_class= CommentSerializer
    permission_classes= [IsAuthenticated]

    # again override perform_create to set product and user 
    def perform_create(self,serializer):
        product_id = self.kwargs.get("pk")
        user = self.request.user
        
        exiting_comment = Comment.objects.filter(product_id=product_id, user=user)
        if exiting_comment.exists():
            raise ValidationError("You have already commented on this product.")

        serializer.save(product_id=product_id, user=user)



class CommentEdit(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this comment.")    
        return obj


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")    
        return obj
