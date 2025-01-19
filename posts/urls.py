from django.urls import path
from .views import CategoryListOrCreateView, CategoryRetrieveUpdateDestroyView, PostListOrCreateView, PostRetrieveUpdateDestroyView
urlpatterns = [
    path('categories/', CategoryListOrCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('posts/', PostListOrCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
]
