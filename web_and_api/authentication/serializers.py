from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from base.models import User
import uuid
import datetime

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super(MyTokenObtainPairSerializer,cls).get_token(user)

    #add custom claims
    token
    return token

class RegisterSerializer(serializers.ModelSerializer):
  # email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
  password = serializers.CharField(write_only = True, required=True, validators=[validate_password])

  class Meta:
    model = User
    exclude=['date_updated','visibility']
  
  def create(self, validated_data):
    user = User.objects.create(
      username = validated_data['username'],
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name'],
      id_number = validated_data['id_number'],
      phone = validated_data['phone'],
      email = validated_data['email'],
      org = validated_data['org'],
      role = validated_data['role'],
      url = uuid.uuid4(),
    )
    user.set_password(validated_data['password'])
    user.save()

    return Response({"status":1, "message":"User created successfully"})
# groups decorator

class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','first_name','last_name', 'id_number', 'phone','email', 'username', 'org', 'date_added', 'url']
    read_only_fields = ('id',)

  def update(self,instance,validated_data):
    instance.first_name = validated_data.get('first_name')
    instance.last_name = validated_data.get('last_name')
    instance.id_number = validated_data.get('id_number')
    instance.phone = validated_data.get('phone')
    instance.email = validated_data.get('email')
    instance.org = validated_data.get('org')
    instance.date_updated = datetime.datetime.now()
    instance.save()
    return instance

  


