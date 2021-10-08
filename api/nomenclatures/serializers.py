from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.nomenclatures.models import Question, AnswerChoice


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, attrs):
        validate = self.validate_strict_type if attrs['type'] == Question.Type.STRICT else self.validate_choice_type
        validate(attrs)
        return attrs

    @staticmethod
    def validate_strict_type(attrs):
        if attrs.get('valid_strict_answer') is None:
            raise ValidationError({'valid_strict_answer': "This field is required"})

    @staticmethod
    def validate_choice_type(attrs):
        if attrs.get('valid_choice') is None:
            raise ValidationError({'valid_choice': "This field is required"})

        if attrs.get('choices') is None:
            raise ValidationError({'choices': "This field is required"})

        if attrs.get('valid_choice') not in attrs.get('choices'):
            raise ValidationError({'valid_choice': "This choice is not in selected choices"})


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ('id', 'title')


class ReturnQuestionSerializer(serializers.ModelSerializer):
    valid_choice = AnswerChoiceSerializer()
    choices = AnswerChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionBaseSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'choices', 'title', 'type', 'points')
