from rest_framework import serializers
from .models import Category,Comment,Like,Post

class CategorySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Category
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerailizer(serializers.ModelSerializer):
    class Meta:
        model =Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True,read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model =Post
        fields = '__all__'

class PostvaluesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'