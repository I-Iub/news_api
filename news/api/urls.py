from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, NewsViewSet

router_v1 = routers.DefaultRouter()
# router_v1.register('users', UserViewSet, basename='users')
router_v1.register('news', NewsViewSet, basename='news')
router_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
