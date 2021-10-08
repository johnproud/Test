from api.core.mixin import BaseModelViewSet
from api.nomenclatures.models import Question, AnswerChoice
from api.nomenclatures.serializers import AnswerChoiceSerializer, QuestionSerializer, ReturnQuestionSerializer


class QuestionViewSets(BaseModelViewSet):
    queryset = Question.objects.all()
    serializer_create_class = QuestionSerializer
    serializer_class = ReturnQuestionSerializer


class AnswerChoiceViewSets(BaseModelViewSet):
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer
