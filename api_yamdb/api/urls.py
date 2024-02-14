from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet
from . import views

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
router_v1.register('categories', views.CategoriesViewSet, basename='categories')
router_v1.register('genres', views.GenresViewSet, basename='genres')
router_v1.register('titles', views.TitlesViewSet, basename='titles')
router_v1.register(r'', UserViewSet, basename='users')

app_name = 'api'
urlpatterns = [
    path('auth/', include(
        [
            path('signup/', views.SignUPView.as_view()),
            path('token/', views.TokenView.as_view()),
        ]
    )),
    path('v1/', include(router_v1.urls)),
]