from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, NewsViewSet, CreateUserViewSet, delete_user

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', CreateUserViewSet, basename='users')
router_v1.register(r'news', NewsViewSet, basename='news')
router_v1.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/users/delete/', delete_user, name='delete_user'),
    path('v1/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
