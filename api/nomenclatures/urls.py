from rest_framework.routers import DefaultRouter

from api.nomenclatures.views import AnswerChoiceViewSets, QuestionViewSets

router = DefaultRouter(trailing_slash=False)
router.register(r'questions', QuestionViewSets, basename='questions')
router.register(r'answer-choices', AnswerChoiceViewSets, basename='answer_choices')
urlpatterns = router.urls
