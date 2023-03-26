from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, News
from .permissions import AuthorOrReadOnly
from .serializers import (CommentSerializer, NewsSerializer,
                          CreateUserSerializer)

User = get_user_model()


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (AuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
