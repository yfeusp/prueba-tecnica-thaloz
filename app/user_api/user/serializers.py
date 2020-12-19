from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import ActivityReport


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=4, max_length=20)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate the credentials"""
        # authenticate the user
        user = authenticate(
            username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        # Save the user in the context
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve token"""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    def validate(self, data):
        """Validate user data"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords do not match.")
        password_validation.validate_password(passwd)

        return data

    def create(self, data):
        """Save the user"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)

        return user


class UserUpdateSerializer(UserCreateSerializer):

    def update(self, instance, data):
        """Update the user"""
        if 'password_confirmation' in data:
            data.pop('password_confirmation')
        if 'password' in data:
            instance.set_password(data['password'])
            data.pop('password')
        # user = User.objects.filter(pk=instance.pk).update(**data)
        for (key, value) in data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class ActivityReportSerializer(serializers.ModelSerializer):

    count = serializers.IntegerField()

    class Meta:
        model = ActivityReport
        fields = ('user', 'date', 'count')
