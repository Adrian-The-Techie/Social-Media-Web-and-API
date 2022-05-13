from django.urls import path
from authentication.views import MyObtainTokenPairView,RegisterView,UserRetrieveUpdateView,AllUsersView, validateEmail, validateUsername
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
  path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
  path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
  path('register/', RegisterView.as_view(), name='register'),
  path('users/', AllUsersView.as_view(), name='all_users'),
  path('user/<str:url>/', UserRetrieveUpdateView.as_view(), name='edit_user'),
  path('validateEmail/', validateEmail, name='validateEmail'),
  path('validateUsername/', validateUsername, name='validateUsername'),
]