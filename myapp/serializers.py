from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WebhookEvent
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

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
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")

        data['user'] = user
        return data

    def save(self):
        password = self.validated_data['new_password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
        return user

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ['event_type', 'reference_id', 'status', 'received_at']
        read_only_fields = ['received_at']
    
    def create(self, validated_data):
        return WebhookEvent.objects.create(**validated_data)