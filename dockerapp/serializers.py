from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','username','email']

class ContainersSerializer(serializers.ModelSerializer):
    print(User)
    class Meta:
        model = DockerContainer
        fields = ['id','owner','image_name','image_tag']
        
