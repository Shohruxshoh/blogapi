from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Post, Category, Comment, PostSave
from .serializers import PostSerializer, CategorySerializer, PostCreateSerializer, PostSaveCreateSerializer, PostSaveSerializer, CommentCreateSerializer, CommentSerializer, CommentUpdateSerializer
from .paginations import CustomPagination
from drf_spectacular.utils import extend_schema_view, extend_schema
# Create your views here.

class CategoryListOrCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class PostListOrCreateView(ListCreateAPIView):
    queryset = Post.objects.select_related('category', 'user').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description', 'category__name', 'user__username']
    pagination_class = CustomPagination


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('category', 'user').all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostSaveListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSaveSerializer

    def get_queryset(self):
        posts = PostSave.objects.filter(user=self.request.user)
        return posts


@extend_schema_view(
    post=extend_schema(
        responses={201: PostSaveSerializer},
        description="Create a new comment for a specific post."
    ),
)
class PostSaveCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, post_id):
        if not post_id:
            return Response({"error": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        post_save, created = PostSave.objects.get_or_create(user=request.user, post=post)
        post_save.is_save = not post_save.is_save
        post_save.save()

        return Response(PostSaveSerializer(post_save).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        responses={200: CommentSerializer(many=True)},
        description="Retrieve the list of comments for a specific post."
    ),
    post=extend_schema(
        request=CommentCreateSerializer,
        responses={201: CommentCreateSerializer},
        description="Create a new comment for a specific post."
    ),
)
class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Foydalanuvchiga tegishli post uchun sharhlarni chiqarish"""
        post_id = self.kwargs.get('pk')
        return Comment.objects.filter(user=self.request.user, post_id=post_id)

    def create(self, request, *args, **kwargs):
        """Yangi sharh yaratish"""
        post_id = self.kwargs.get('pk')
        print(109, post_id)

        # Post mavjudligini tekshirish
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = request.user.id
        data['post'] = post.id

        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@extend_schema_view(
    get=extend_schema(
        responses={200: CommentSerializer(many=True)},
        description="Retrieve the list of comments for a specific post."
    ),
    put=extend_schema(
        request=CommentUpdateSerializer,
        responses={201: CommentSerializer},
        description="Create a new comment for a specific post."
    ),
    patch=extend_schema(
        request=CommentUpdateSerializer,
        responses={201: CommentSerializer},
        description="Create a new comment for a specific post."
    ),
)
class CommentRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentUpdateSerializer(comment, data=request.data,  partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

