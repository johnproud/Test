# from api.users.models import CustomUser
from django.db import models
from django.utils.translation import gettext as _
from parler.models import TranslatableModel
from softdelete.managers import SoftDeleteManager
from softdelete.models import SoftDeleteModel

from api.core.managers import SoftDeleteTranslatableDotsManager


class BaseModelMixin(SoftDeleteModel):
    objects = SoftDeleteManager()
    created_by = models.ForeignKey(
        "users.User",  # noqa
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Creator'),
        related_name='%(class)s_create_user'
    )
    updated_by = models.ForeignKey(
        "users.User",  # noqa
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Editor'),
        related_name='%(class)s_update_user'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    @property
    def created(self):
        """
        Return the created_at datetime text by selected format.
        """
        return self.created_at.strftime('%d/%m/%Y %H:%I:%S')


class BaseTranslatableModelMixin(TranslatableModel, BaseModelMixin):
    objects = SoftDeleteTranslatableDotsManager()
    created_by = models.ForeignKey(
        "users.User",  # noqa
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Creator'),
        related_name='%(class)s_create_user'
    )
    updated_by = models.ForeignKey(
        "users.User",  # noqa
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Editor'),
        related_name='%(class)s_update_user'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ["id"]

    @property
    def created(self):
        """
        Return the created_at datetime text by selected format.
        """
        return self.created_at.strftime('%d/%m/%Y %H:%I:%S')
