import json
import os

from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext as _
from rest_framework import serializers

from api.core.exceptions import BaseValidationError
from api.core.helper import get_filters_by_conditions
from api.users.models import User


class UniqueValidators(object):
    @staticmethod
    def unique_user_email(value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise serializers.ValidationError({'email': [_('such email already exist')]})


class TranslatableValidators(object):
    @staticmethod
    def field(value):
        if type(value) is not dict:
            try:
                value = json.loads(value)
            except Exception as e:  # Todo some certain exception
                raise serializers.ValidationError('%s incorrect json format' % value)
        if isinstance(value, dict):
            if value.get('ro', None) is None:
                raise serializers.ValidationError('%(value)s does not have default ro translation' % {'value': value})
        else:
            raise serializers.ValidationError('%(value)s does not have default ro translation' % {'value': value})


class FileValidators(object):
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160

    @staticmethod
    def validate_image(value):
        file_name, file_extension = os.path.splitext(value.name)
        if file_extension != '.png' and file_extension != '.jpg' and file_extension != '.jpeg':
            raise serializers.ValidationError("We don't support %(fileExtension)s  for Image %(filename)s" %
                                              {'fileExtension': file_extension, 'filename': file_name})

    @staticmethod
    def validate_file(value):
        if int(value.size) > 20971520:
            raise serializers.ValidationError(
                _("Please keep file size under %(filesize)s. Current file size %(current_filesize)s") % {
                    'filesize': filesizeformat(20971520), 'current_filesize': filesizeformat(value.size)
                }
            )

    @staticmethod
    def validate_csv_file(value):
        file_extension = os.path.splitext(value.name)
        if file_extension[1] != '.csv':
            raise serializers.ValidationError(_('File must be of type csv'))

        if int(value.size) > 20971520:
            raise serializers.ValidationError(
                _("Please keep file size under %(filesize)s. Current file size %(current_filesize)s") % {
                    'filesize': filesizeformat(20971520), 'current_filesize': filesizeformat(value.size)
                })


def is_true(value):
    if not value:
        raise serializers.ValidationError(_('This field must be True'))

    return value
