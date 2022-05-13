import uuid
import rsa
import os
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from base.models import AccessKeysAndTokens, Organisation, User
from base.serializer import OrganisationSerializer
from .serializers import UserSerializer, AccessKeysAndTokensSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from base.api_general import genErrorMsg, genTweepyAuthAndCallAPI, getPrivateKey, getUser

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.filter(visibility=True)
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            token = request.headers['Authorization'].split(sep=" ", maxsplit=2)[
                1]
            user = getUser(token)
            userInstance = User.objects.create(
                username=request.data['username'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                id_number=request.data['id_number'],
                phone=request.data['phone'],
                email=request.data['email'],
                org=user.org,
                role=request.data['role'],
                url=uuid.uuid4(),
            )
            userInstance.set_password(request.data['password'])
            userInstance.save()

            response = {
                "status": 1,
                "data": "User created successfully"
            }
        except Exception as e:
            response = {'status': 0, "message": '{}'.format(e)}

        return Response(response)


class UserRetrieveUpdateView(APIView):
    def get(self, request, url, format=None):
        user = get_object_or_404(User, url=url)
        serializer = UserSerializer(user)
        response = {
            "status": 1,
            "data": serializer.data
        }

        return Response(response)

    def put(self, request, url, format=None):
        response = {}
        try:
            user = get_object_or_404(User, url=url)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": 1,
                    "data": "User updated successfully"
                }
                return Response(response)
            else:
                raise Exception(serializer.errors)
        except Exception as e:
            response = {'status': 0, "message": '{}'.format(e)}
        return Response(response)

    def delete(self, request, url, format=None):
        try:
            user = get_object_or_404(User, url=url)
            user.visibility = False
            user.save()
            return Response({'status': 1, 'message': 'User deleted successfully'})
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})


class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = request.headers['Authorization'].split(sep=" ", maxsplit=2)[
                1]
            user = getUser(token)
            all_users = User.objects.filter(
                visibility=True, org=user.org).order_by('id')
            serializer = UserSerializer(all_users, many=True)
            return Response({"status": 1, "data": serializer.data})
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})


@api_view(['POST'])
def validateEmail(request):
    try:
        emailInstance = User.objects.filter(email=request.data['email'])
        if(len(emailInstance) > 0):
            raise Exception(
                'There seems to be an user with that email. Please choose a unique email')
        else:
            return Response({'status': 1, "message": 'Proceed'})
    except Exception as e:
        return Response({'status': 0, "message": '{}'.format(e)})


@api_view(['POST'])
def validateUsername(request):
    try:
        usernameInstance = User.objects.filter(
            username=request.data['username'])
        if(len(usernameInstance) > 0):
            raise Exception(
                'There seems to be an user with that username. Please choose a unique username')
        else:
            return Response({'status': 1, "message": 'Proceed'})
    except Exception as e:
        return Response({'status': 0, "message": '{}'.format(e)})

# PAGES API


@api_view(['POST'])
def validatePageName(request):
    try:
        pageNameInstance = AccessKeysAndTokens.objects.filter(
            page_name=request.data['pageName'])
        if(len(pageNameInstance) > 0):
            raise Exception(
                'There seems to be an page with that name. Please choose a unique name')
        else:
            return Response({'status': 1, "message": 'Proceed'})
    except Exception as e:
        return Response({'status': 0, "message": '{}'.format(e)})


class RegisterPage(generics.CreateAPIView):
    queryset = AccessKeysAndTokens.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AccessKeysAndTokensSerializer

    def post(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization'].split(sep=" ", maxsplit=2)[
                1]
            user = getUser(token)
            org = Organisation.objects.get(id=user.org)

            # # encrypt api_key, api_key_secret and bearer tokens
            pub_key = rsa.PublicKey(
                int(os.environ.get('N')), int(os.environ.get('E')))
            twitter_api_key = request.POST['api_key']
            twitter_api_key_secret = request.POST['api_key_secret']
            twitter_access_token = request.POST['access_token']
            twitter_access_token_secret = request.POST['access_token_secret']
            twitter_bearer_token = request.POST['bearer_token']

            pageInstance = AccessKeysAndTokens(
                org=org,
                page_name=request.POST['pageName'],
                twitter_api_key=twitter_api_key,
                twitter_api_key_secret=twitter_api_key_secret,
                twitter_access_token=twitter_access_token,
                twitter_access_token_secret=twitter_access_token_secret,
                twitter_bearer_token=twitter_bearer_token,
                created_by=user.id,
                url=uuid.uuid4())
            pageInstance.save()
            return Response({"status": 1, "message": "Page credentials added successfully"})
        except Exception as e:
            return Response({"status": 0, "message": "{}. {}".format(genErrorMsg('adding page credentials'), e)})


class TwitterPages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        token = request.headers['Authorization'].split(sep=" ", maxsplit=2)[
            1]
        user = getUser(token)
        org = Organisation.objects.get(id=user.org)
        try:
            all_pages = AccessKeysAndTokens.objects.filter(
                visibility=True, org=org).order_by('id')
            serializers = AccessKeysAndTokensSerializer(all_pages, many=True)
            serializedPages = serializers.data
            for serializedPage in serializedPages:
                serializedPage['created_by'] = User.objects.get(
                    id=serializedPage['created_by']).username
                # org['date_added']=genDateTimeString(org['date_added'])
            response = {
                'status': 1,
                'data': serializedPages
            }
            return Response(response)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})


class TwitterPageRetrieveUpdate(APIView):
    def get(self, request, url, format=None):
        try:
            page = AccessKeysAndTokens.objects.filter(url=url).values().first()
            page['created_by'] = User.objects.get(
                id=page['created_by']).username
            response = {
                "status": 1,
                "data": page
            }
            # get account settings
            # api = genTweepyAuthAndCallAPI(page)

            return Response(response)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})

    def put(self, request, url, format=None):
        try:
            values = get_object_or_404(AccessKeysAndTokens, url=url)
            serializer = AccessKeysAndTokensSerializer(values, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 1,
                    'message': 'Values updated successfully'
                }
                return Response(response)
            else:
                raise Exception(serializer.errors)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})

    def delete(self, request, url, format=None):
        try:
            property = get_object_or_404(AccessKeysAndTokens, url=url)
            property.visibility = 0
            property.save()
            return Response({'status': 1, 'message': 'Organisation deleted successfully'})
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})

    def loadTrends(self, request):
         
