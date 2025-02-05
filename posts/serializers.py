from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'name', 'description', 'image']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['category', 'name', 'description', 'image']


class PostSaveSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    class Meta:
        model = PostSave
        fields = ['id', 'post', 'is_save']

class PostSaveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSave
        fields = ['is_save']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'user', 'message']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post','message']
    
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message']


