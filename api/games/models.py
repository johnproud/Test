from django.db import models
from django.db.models import PROTECT

from api.core.models import BaseModelMixin
from api.nomenclatures.models import Question, Response


class Game(BaseModelMixin):
    title = models.CharField(max_length=200)
    description = models.TextField()
    questions = models.ManyToManyField(Question)

    class Meta:
        db_table = 'games'


class GameResult(BaseModelMixin):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress'
        COMPLETED = 'completed'

    game = models.ForeignKey(Game, on_delete=PROTECT)
    status = models.CharField(max_length=150, choices=Status.choices, default=Status.IN_PROGRESS)
    unanswered_questions = models.IntegerField()
    answered_questions = models.IntegerField()
    responses = models.ManyToManyField(Response)
    earned_points = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'game_results'
