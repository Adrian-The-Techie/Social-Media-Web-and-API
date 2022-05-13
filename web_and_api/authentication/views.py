from functools import partial
from django.core.exceptions import ObjectDoesNotExist
from django.http import response
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, decorators

from base import serializer
from .serializers import MyTokenObtainPairSerializer,RegisterSerializer,UserRetrieveUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from base.models import User
from .permissions import IsStaff


# Create your views here.

class MyObtainTokenPairView(TokenObtainPairView):
  permission_classes = (AllowAny,)
  serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
  queryset = User.objects.filter(visibility=True)
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class UserRetrieveUpdateView(APIView):
  def get(self, request, url, format = None):
    user = get_object_or_404(User, url =url)
    serializer = UserRetrieveUpdateSerializer(user)
    response={
      "status":1,
      "data":serializer.data
    }
    return Response(response)

  def put(self,request,url, format = None):
    try:
      user = get_object_or_404(User, url=url)
      serializer = UserRetrieveUpdateSerializer(user, data=request.data)
      if serializer.is_valid():
        serializer.save()
        response={
          "status":1,
          "data":"User updated successfully"
        }
        return Response(response)
    except Exception as e:
      return Response({'status':0, "message":'{}'.format(e)})


  def delete(self,request,url, format = None):
    try:
      user = get_object_or_404(User, url =url)
      user.visibility = False
      user.save()
      return Response({'status':1,'message': 'User deleted successfully'})
    except Exception as e:
      return Response({'status':0, "message":'{}'.format(e)})

class AllUsersView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self,request):
    try:
      all_users = User.objects.filter(visibility=True).order_by('id')
      serializer = UserRetrieveUpdateSerializer(all_users, many = True)
      return Response({"status":1,"data":serializer.data})
    except Exception as e:
      return Response({'status':0, "message":'{}'.format(e)})

@decorators.api_view(['POST'])
def validateEmail(request):
  try:
    emailInstance=User.objects.filter(email=request.data['email'])
    if(len(emailInstance)>0):
      raise Exception('There seems to be an user with that email. Please choose a unique email')
    else:
      return Response({'status':1, "message":'Proceed'})
  except Exception as e:
    return Response({'status':0, "message":'{}'.format(e)})

@decorators.api_view(['POST'])
def validateUsername(request):
  try:
    usernameInstance=User.objects.filter(username=request.data['username'])
    if(len(usernameInstance)>0):
      raise Exception('There seems to be an user with that username. Please choose a unique username')
    else:
      return Response({'status':1, "message":'Proceed'})
  except Exception as e:
    return Response({'status':0, "message":'{}'.format(e)})