from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.inspectors.base import call_view_method
from drf_yasg.utils import no_body
from pendulum import now
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from api.core.pagination import CustomPagination
from api.core.permissions import IsAdmin


class CreateBaseModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_obj = self.perform_create(serializer)
        serializer_display = self.get_serializer(model_obj)
        headers = self.get_success_headers(serializer_display.data)
        return Response({"data": serializer_display.data}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):  # noqa
        return serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

    def get_success_headers(self, data):  # noqa
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateBaseModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # noqa
        serializer = self.get_serializer_create(instance, data=request.data, partial=partial)  # noqa
        serializer.is_valid(raise_exception=True)
        model_obj = self.perform_update(serializer)
        serializer_display = self.get_serializer(model_obj)  # noqa

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'data': serializer_display.data})

    def perform_update(self, serializer):  # noqa
        return serializer.save(updated_by=self.request.user if self.request.user.is_authenticated else None)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RetrieveBaseModelMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data})


class ListBaseModelMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    @action(detail=False, url_path='list')
    def list_dropdown(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})


class GenericBaseViewSet(GenericViewSet):
    serializer_create_class = None
    permission_classes_by_action = {
        'default': [IsAdmin]
    }
    action_serializers = {}
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    serializer_query_class = None
    ordering = ['id']
    filter_fields = []
    permission_classes = [IsAdmin]
    filter_by_owner = False

    def get_serializer_class(self):
        if self.action in self.action_serializers:
            return self.action_serializers[self.action]

        return super().get_serializer_class()

    def get_paginated_response(self, data, json=False):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, json)

    def get_permissions(self):
        assert 'default' in self.permission_classes_by_action, (
                "'%s' should include a `default` attribute in permission_classes_by_action "
                % self.__class__.__name__
        )
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            if self.permission_classes:
                return [permission() for permission in self.permission_classes]
            return [permission() for permission in self.permission_classes_by_action['default']]

    def get_serializer_create(self, *args, **kwargs):
        serializer_class = self.get_serializer_create_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_create_class(self):

        return self.serializer_create_class if self.serializer_create_class is not None else self.serializer_class

    def get_query_serializer(self):
        if self.action == ['retrieve', 'post', 'patch']:
            return None
        return self.serializer_query_class


class DestroyBaseModelMixin:

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.save(deleted_at=now())


class BaseModelViewSet(
    RetrieveBaseModelMixin,
    DestroyBaseModelMixin,
    ListModelMixin,
    CreateBaseModelMixin,
    UpdateBaseModelMixin,
    GenericBaseViewSet
):
    pagination_class = CustomPagination


class CustomAutoSchema(SwaggerAutoSchema):
    def get_view_response_serializer(self):
        return call_view_method(self.view, 'get_serializer')

    def get_view_serializer(self):
        if call_view_method(self.view, 'get_serializer_create'):
            return call_view_method(self.view, 'get_serializer_create')
        return call_view_method(self.view, 'get_serializer')

    def get_view_query_serializer(self):
        return call_view_method(self.view, 'get_query_serializer')

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self.get_view_response_serializer()

    def get_query_serializer(self):
        if self.overrides.get('query_serializer', None) is None:
            self.overrides['query_serializer'] = self.get_view_query_serializer()
        return super(CustomAutoSchema, self).get_query_serializer()
