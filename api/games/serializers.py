from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.games.models import Game, GameResult
from api.nomenclatures.models import Response, Question
from api.nomenclatures.serializers import QuestionBaseSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("title", 'questions')


class ReturnGameSerializer(serializers.ModelSerializer):
    questions = QuestionBaseSerializer(many=True)

    class Meta:
        model = Game
        fields = ("title", "id", 'questions')


class ReturnBaseGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("title", "id")


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ("question", 'choice_response', 'strict_response')


class ReturnResponseSerializer(serializers.ModelSerializer):
    choice_response = serializers.CharField(source='choice_response.title')
    question = serializers.CharField(source='question.title')

    class Meta:
        model = Response
        fields = ("question", 'choice_response', 'strict_response')


class ReturnGameResultSerializer(serializers.ModelSerializer):
    responses = ReturnResponseSerializer(many=True)
    game = ReturnBaseGameSerializer()

    class Meta:
        model = GameResult
        fields = ("id", "game", 'responses', 'status', 'unanswered_questions', 'answered_questions', 'earned_points')


class GameResultSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True)

    class Meta:
        model = GameResult
        fields = ("game", 'responses')

    def create(self, validated_data):
        responses = self.create_or_update_responses(validated_data)
        GameResult.objects.filter(game=validated_data['game'], is_active=True).update(is_active=False)
        result = super(GameResultSerializer, self).create(validated_data)
        result.responses.set(responses)
        return result

    def create_or_update_responses(self, validated_data):
        game_questions = set(validated_data['game'].questions.values_list('id', flat=True))
        response_question_ids = set(map(lambda x: x['question'].id, validated_data['responses']))
        question_differences = response_question_ids.difference(game_questions)
        responses = []
        total_points = 0

        if question_differences:
            raise ValidationError({"responses": f"questions with ids {str(question_differences)} "
                                                f"are not for this game"})
        for response in validated_data.pop('responses'):
            if response['question'].type == Question.Type.STRICT and response.get('strict_response') is None:
                raise ValidationError({"responses": f"questions with id {response['question'].id} "
                                                    f"has invalid answer"})

            if response['question'].type == Question.Type.CHOICES and response.get('choice_response') is None:
                raise ValidationError({"responses": f"questions with id {response['question'].id} "
                                                    f"has invalid answer"})

            if (
                    response['question'].valid_choice == response.get('choice_response') or
                    response['question'].valid_strict_answer == response.get('strict_response')
            ):
                response['points_earned'] = response['question'].points
                response['is_valid_response'] = True
            else:
                response['points_earned'] = 0
                response['is_valid_response'] = False

            obj, _ = Response.objects.update_or_create(
                game=validated_data['game'],
                question=response.pop('question'),
                created_by=self.context['request'].user,
                defaults=response
            )
            total_points += response['points_earned']
            responses.append(obj)

        if len(response_question_ids) == len(game_questions):
            validated_data['status'] = GameResult.Status.COMPLETED

        validated_data['unanswered_questions'] = len(game_questions.difference(response_question_ids))
        validated_data['answered_questions'] = len(response_question_ids)
        validated_data['earned_points'] = total_points
        return responses
