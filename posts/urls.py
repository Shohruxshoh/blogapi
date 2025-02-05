from django.urls import path
from .views import CategoryListOrCreateView, CategoryRetrieveUpdateDestroyView, PostListOrCreateView, PostRetrieveUpdateDestroyView, \
PostSaveListView, PostSaveCreateView, CommentListCreateView, CommentRetrieveUpdateDestroyView
urlpatterns = [
    path('categories/', CategoryListOrCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('posts/', PostListOrCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
    path('post-save/', PostSaveListView.as_view(), name='post-save'),
    path('post-save-create/<int:post_id>', PostSaveCreateView.as_view(), name='post-save-create'),

    path('comments/<int:pk>', CommentListCreateView.as_view(), name='comments'),
    path('comments/datail/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
]
