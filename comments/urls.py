from django.urls import path
from .views import *

urlpatterns = [
    path('product/<int:pk>/', CommentList.as_view(), name='comment_list'),
    path('<int:pk>/create/', CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/edit/', CommentEdit.as_view(), name='comment_edit'),
    path('<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),

    path('admin/',AdminCommentList.as_view(), name='admin_comment_list'),
    path('admin/product/<int:pk>/', AdminCommentList.as_view(), name='admin_comment_list_product'),
    path('admin/<int:pk>/edit/', AdminCommentEdit.as_view(), name='admin_comment_edit'),
    path('admin/<int:pk>/delete/', AdminCommentDelete.as_view(), name='admin_comment_delete'),
 ]

#comments/product/1
#comments//create/1  -> create comment
#commnets/1/edit -> edit comment
#comments/1/delete -> delete comment

