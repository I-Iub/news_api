import datetime
import os

from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.utils import timezone as django_timezone
from rest_framework import serializers

from .models import Comment, News

load_dotenv()
weeks = int(os.getenv('CONSTRAINT_LIFETIME_WEEKS'))
delta = datetime.timedelta(weeks=weeks)

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'text', 'author', 'news', 'published')
        read_only_fields = ['author', 'published']


class NewsSerializer(serializers.ModelSerializer):
    num_comments = serializers.IntegerField(read_only=True)
    comments_ = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('pk', 'title', 'text', 'author', 'likes', 'published',
                  'num_comments', 'comments_')
        read_only_fields = ['author', 'likes', 'published']

    def validate_title(self, title):
        now = django_timezone.now()
        request = self.context.get('request')
        user = None
        if request is not None and hasattr(request, 'user'):
            user = request.user
        if user is None:
            raise serializers.ValidationError(
                'В объекте запроса `request` должен быть указан пользователь '
                '`user`'
            )
        if News.objects.filter(
                title=title,
                author=user,
                published__gt=(now - delta)).exists():
            raise serializers.ValidationError(
                'За последний период %s недель(и) Вы уже публиковали '
                'новость с таким заголовком.' % weeks
            )
        return title


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk', 'username', 'password', 'first_name', 'last_name', 'email'
        )

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
