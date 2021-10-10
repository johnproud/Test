from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.core.mixin import BaseModelViewSet, GenericBaseViewSet, CreateBaseModelMixin, UpdateBaseModelMixin
from api.users.models import User
from api.users.serializers import UserSerializer, UserRegisterSerializer


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserViewSet(
    ListModelMixin,
    UpdateBaseModelMixin,
    GenericBaseViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {"default": [IsAuthenticated]}

    def list(self, request, *args, **kwargs):
        """ 
           This endpoint will return current logged user
        """
        return Response(UserSerializer(request.user).data)


class UserRegister(CreateBaseModelMixin, GenericBaseViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):  # noqa
        return serializer.save()
