from rest_framework import serializers

from .models import Comment, News


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'text', 'author', 'news', 'published')


class NewsSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    published = serializers.DateTimeField(read_only=True)

    class Meta:
        model = News
        fields = ('pk', 'title', 'text', 'author', 'likes', 'published')
