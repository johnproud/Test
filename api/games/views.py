from django.db.models import F, Subquery, Sum, OuterRef
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.core.mixin import BaseModelViewSet
from api.core.permissions import IsAdmin
from api.games.models import Game, GameResult
from api.games.serializers import GameSerializer, ReturnGameSerializer, GameResultSerializer, ReturnGameResultSerializer
from api.users.models import User
from api.users.serializers import UserRankSerializer


class GameViewSet(BaseModelViewSet):
    queryset = Game.objects.all()
    serializer_create_class = GameSerializer
    serializer_class = ReturnGameSerializer
    permission_classes_by_action = dict(
        default=[IsAdmin],
        play=[IsAuthenticated],
        rank=[IsAuthenticated],
        rank_for_all=[IsAuthenticated],
    )

    @action(detail=False, queryset=GameResult.objects.all(), methods=['POST'],
            serializer_class=ReturnGameResultSerializer,
            serializer_create_class=GameResultSerializer)
    def play(self, request):
        """
           Endpoint for start to play a game.
        """
        return self.create(request)

    @action(detail=True, queryset=User.objects.all(), methods=['GET'],
            serializer_class=UserRankSerializer)
    def rank(self, request, **kwargs):
        """
           Rank for certain game. will get users which played this game ordered by points yarned
        """
        users = User.objects.alias(
            points=Subquery(GameResult.objects.filter(
                game=kwargs['pk'], is_active=True,
                created_by=OuterRef('id')
            ).order_by('-earned_points')[:1].values('earned_points')),
        ).annotate(points=F('points')).order_by("-points")
        return Response(UserRankSerializer(users, many=True).data)

    @action(detail=False, queryset=User.objects.all(), methods=['GET'], url_path='rank',
            serializer_class=UserRankSerializer)
    def rank_for_all(self, request):
        """
           Rank for all games. This endpoint will get best users for all games
        """
        users = User.objects.alias(
            points=Subquery(GameResult.objects.filter(
                is_active=True,
                created_by=OuterRef('id')
            ).values('earned_points').annotate(points_sum=Sum('earned_points'))[:1].values('points_sum')),
        ).annotate(points=F('points')).order_by("-points")
        return Response(UserRankSerializer(users, many=True).data)
