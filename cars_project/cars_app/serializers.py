from rest_framework import serializers
from .models import Car, Comment

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'car']
        read_only_fields = ['id', 'created_at', 'author', 'car']