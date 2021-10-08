from rest_framework.routers import DefaultRouter
from api.users.views import UserViewSet, UserRegister, CurrentUserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'me', CurrentUserViewSet, basename='me')
router.register(r'register', UserRegister, basename='register')
urlpatterns = router.urls
