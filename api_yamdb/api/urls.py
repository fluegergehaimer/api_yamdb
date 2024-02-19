"""Api urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)
router_v1.register(
    'categories',
    views.CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    views.GenresViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    views.TitlesViewSet,
    basename='titles'
)
router_v1.register(r'users', views.UserViewSet, basename='users',)

urlpatterns = [
    path(
        'v1/auth/signup/',
        views.RegistrationAPIView.as_view(),
        name='signup'
    ),
    path(
        'v1/auth/token/',
        views.AuthenticationAPIView.as_view(),
        name='token'
    ),
    path('v1/', include(router_v1.urls)),
]


###
# from django.urls import include, path
# from rest_framework import routers


# app_name = 'users'

# router_v1 = routers.DefaultRouter()
# router_v1.register(r'', UserViewSet, basename='users',)

# urlpatterns = [
#     path('v1/auth/signup/', RegistrationAPIView.as_view(), name='signup'),
#     path('v1/auth/token/', AuthenticationAPIView.as_view(), name='token'),
#     path('v1/users/', include(router_v1.urls)),
#     path('', include('api.urls')),
# ]
