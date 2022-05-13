from django.urls import path
from .views import *

urlpatterns = [
    path('users', AllUsersView.as_view(), name="all_users"),
    path('user/<uuid:url>/', UserRetrieveUpdateView.as_view(), name="user"),
    path('addUser/', RegisterView.as_view(), name="addUser"),
    path('addPageCredentials/', RegisterPage.as_view()),
    path('twitterPages', TwitterPages.as_view(), name="my_twitter_pages"),
    path('twitterPages/<uuid:url>/',
         TwitterPageRetrieveUpdate.as_view(), name="my_twitter_page"),
    path('validatePageName/', validatePageName, name='validatePage'),
]
