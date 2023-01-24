from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories',views.CategoryViewSet,basename='category')
router.register('comments',views.CommentViewSet,basename='comments')
router.register('likes',views.LikeViewSet,basename='likes')
router.register('posts',views.PostViewSet,basename='posts')
urlpatterns = [
    path('',include(router.urls))
]
