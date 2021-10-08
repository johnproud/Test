from django.db import models
from django.db.models import PROTECT
from parler.models import TranslatableModel

from api.core.models import BaseTranslatableModelMixin, BaseModelMixin


class AnswerChoice(BaseModelMixin):
    title = models.CharField(max_length=300)

    class Meta:
        ordering = ['id']
        db_table = 'answer_choices'


class Question(BaseModelMixin):
    class Type(models.TextChoices):
        CHOICES = 'choices'
        STRICT = 'strict'

    title = models.CharField(max_length=300)
    type = models.CharField(max_length=150, choices=Type.choices, default=Type.STRICT)
    points = models.IntegerField()

    choices = models.ManyToManyField(AnswerChoice, blank=True, related_name='_questions')
    valid_choice = models.ForeignKey(AnswerChoice, on_delete=PROTECT, null=True, related_name='valid_questions')
    valid_strict_answer = models.BooleanField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'questions'


class Response(BaseModelMixin):
    question = models.ForeignKey(Question, on_delete=PROTECT)
    choice_response = models.ForeignKey(AnswerChoice, on_delete=PROTECT, null=True)
    strict_response = models.BooleanField(null=True)
    is_valid_response = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    game = models.ForeignKey("games.Game", on_delete=PROTECT, related_name='responses')

    class Meta:
        ordering = ['id']
        db_table = 'responses'
