from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('blogs', views.BlogView, basename='blogs')

urlpatterns = [
    # path('homeblogs/', views.HomeBlog.as_view(), name='homeblogs')
]

urlpatterns += router.urls