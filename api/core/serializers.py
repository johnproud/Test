import json

from parler_rest.serializers import TranslatableModelSerializer
from rest_framework import serializers


class BaseTranslatableModelSerializer(TranslatableModelSerializer):
    def save_translations(self, instance, translated_data):
        if type(translated_data) is not dict:
            translated_data = json.loads(translated_data)
        for meta in self.Meta.model._parler_meta:  # noqa
            for field_name, translations in translated_data.items():
                if type(translations) is not dict:
                    translations = json.loads(translations)
                for lang_code, translation in translations.items():
                    if field_name in meta.get_translated_fields():
                        instance.set_current_language(lang_code)
                        setattr(instance, field_name, translation)  # TODO refactoring
                        instance.save()


class BaseSerializer(serializers.Serializer):
    def create(self, validated_data):
        ...

    def update(self, instance, validated_data):
        ...
