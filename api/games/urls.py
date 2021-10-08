from rest_framework.routers import DefaultRouter
from api.games.views import GameViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'games', GameViewSet, basename='game')
urlpatterns = router.urls
