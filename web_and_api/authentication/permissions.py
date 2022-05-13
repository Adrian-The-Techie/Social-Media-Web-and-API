from django.http import response
from rest_framework import permissions
from rest_framework.response import Response
from django.conf import settings
from base.models import User
from base.api_general import getUser



class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        # # get Authorization header
        token= request.headers['Authorization'].split(sep=" ", maxsplit=2)[1]
        user=getUser(token)
        if user.is_staff: 
            return True
        return False
    