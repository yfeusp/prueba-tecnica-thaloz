from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserLoginSerializer, UserModelSerializer,
    UserCreateSerializer, UserUpdateSerializer, ActivityReportSerializer,
    ActivityReportDaySerializer, ActivityReportMonthSerializer)
from .models import ActivityReport
from .mixins import MixedPermissionMixin


class UserViewSet (MixedPermissionMixin, viewsets.ModelViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny]}

    @action(
        detail=False, methods=['post'],
        permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
       
        # Save activity report
        ActivityReport.objects.create(user=user)

        data = {
             'user': UserModelSerializer(user).data,
             'access_token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid user id.'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)


class ActivityReportViewSet (viewsets.GenericViewSet):

    queryset = ActivityReport.objects.all()
    serializer_class = ActivityReportSerializer

    @action(detail=False, methods=['get'])
    def day(self, request):
        query = ActivityReport.objects.all().values(
            'user__username', 'date'
        ).annotate(count=Count('date')).order_by('date')

        serializer = ActivityReportDaySerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def month(self, request):
        query = ActivityReport.objects.all().values(
            'user__username', 'date'
        ).annotate(count=Count('date__month')).order_by('date')

        serializer = ActivityReportMonthSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
