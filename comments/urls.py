from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/product', CommentListView.as_view(), name='comments_by_product'),
    path('<int:pk>', CommentDetailsView.as_view(), name='comments_details'),
    path('<int:pk>/delete', CommentDeleteView.as_view(), name='comments_delete'),
]