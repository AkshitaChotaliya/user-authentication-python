from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data['username_or_email']
        password = data['password']

        try:
            user_obj = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        data['user'] = user
        return data
        
class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        try:
            token_obj = Token.objects.get(key=token)
            data['token_obj'] = token_obj
        except Token.DoesNotExist:
            raise serializers.ValidationError("Invalid token")
        return data
