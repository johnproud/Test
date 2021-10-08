from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.games.models import GameResult
from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'total_points')

    @staticmethod
    def get_total_points(obj):
        return GameResult.objects.filter(
                is_active=True, created_by=obj
            ).aggregate(total_points=Sum('earned_points'))['total_points']


class UserRankSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'points')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
