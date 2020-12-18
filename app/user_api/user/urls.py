from django.urls import include, path
from rest_framework.routers import DefaultRouter
from user import views as user_views

router = DefaultRouter()
router.register(r'user', user_views.UserViewSet, basename='user')
router.register(
    r'activityReport', user_views.ActivityReportViewSet,
    basename='activityReport')

urlpatterns = [
    path('', include(router.urls)),
]
