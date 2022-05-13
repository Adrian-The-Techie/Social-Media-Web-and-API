from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^api/org/$', views.OrgList.as_view()),
    url(r'^api/createOrg/$', views.RegisterOrg.as_view()),
    path('api/org/<uuid:url>', views.OrgRetrieveUpdate.as_view()),
    path('api/validateOrg/', views.validateOrg, name='validateOrg'),

]
