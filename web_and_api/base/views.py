import uuid
from rest_framework.permissions import IsAuthenticated
import rsa
import os
from dotenv import load_dotenv
from django.conf import settings
from django.http import response
from django.shortcuts import get_object_or_404, render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from base.api_general import genErrorMsg, getUser

from authentication.permissions import IsStaff
from .models import Organisation, User, AccessKeysAndTokens
from .serializer import OrganisationSerializer
# Create your views here.

# ORGANISATION MODULE


@api_view(['POST'])
def validateOrg(request):
    try:
        orgInstance = Organisation.objects.filter(name=request.data['name'])
        if(len(orgInstance) > 0):
            raise Exception(
                'There seems to be an organisation with that name. Please choose a unique name')
        else:
            return Response({'status': 1, "message": 'Proceed'})
    except Exception as e:
        return Response({'status': 0, "message": '{}'.format(e)})


class RegisterOrg(generics.CreateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = [IsStaff]
    serializer_class = Organisation

    def post(self, request, *args, **kwargs):
        try:
            token = request.headers['Authorization'].split(sep=" ", maxsplit=2)[
                1]
            createdBy = getUser(token)
            orgInstance = Organisation(
                name=request.POST['name'], created_by=createdBy, url=uuid.uuid4())
            orgInstance.save()
            return Response({"status": 1, "message": "Organisation created successfully"})
        except Exception as e:
            return Response({"status": 0, "message": "{}. {}".format(genErrorMsg('creating organisation'), e)})


class OrgList(APIView):
    permission_classes = [IsStaff]

    def get(self, request, format=None):
        try:
            all_property = Organisation.objects.filter(
                visibility=True).order_by('id')
            serializers = OrganisationSerializer(all_property, many=True)
            orgs = serializers.data
            for org in orgs:
                org['created_by'] = User.objects.get(
                    id=org['created_by']).username
                # org['date_added']=genDateTimeString(org['date_added'])
            response = {
                'status': 1,
                'data': orgs
            }
            return Response(response)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})


class OrgRetrieveUpdate(APIView):
    def get(self, request, url, format=None):
        try:
            property = get_object_or_404(Organisation, url=url)
            serializer = OrganisationSerializer(property)
            response = {
                "status": 1,
                "data": serializer.data
            }
            response['data']['created_by'] = User.objects.get(
                id=response['data']['created_by']).username

            return Response(response)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})

    def put(self, request, url, format=None):
        try:
            property = get_object_or_404(Organisation, url=url)
            serializer = OrganisationSerializer(property, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 1,
                    'message': 'Organisation updated successfully'
                }
                return Response(response)
            else:
                raise Exception(serializer.errors)
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})

    def delete(self, request, url, format=None):
        try:
            property = get_object_or_404(Organisation, url=url)
            property.visibility = 0
            property.save()
            return Response({'status': 1, 'message': 'Organisation deleted successfully'})
        except Exception as e:
            return Response({'status': 0, "message": '{}'.format(e)})
