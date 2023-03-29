from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Like, News
from .permissions import AuthorOrReadOnly
from .serializers import (CommentSerializer, NewsSerializer,
                          CreateUserSerializer)

User = get_user_model()


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly | IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.annotate(num_comments=Count('comments')).all()
    serializer_class = NewsSerializer
    permission_classes = (AuthorOrReadOnly | IsAdminUser,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(url_path='like', url_name='like', detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            like = Like.objects.create(user=request.user, news=news)
            like.save()
        except IntegrityError:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        news.likes += 1
        return Response(status=status.HTTP_201_CREATED)


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


@api_view(['delete'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = User.objects.get(username=request.user.username)
        user.delete()
    except User.DoesNotExists:
        pass
    return Response(status=status.HTTP_204_NO_CONTENT)
