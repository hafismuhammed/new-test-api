from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', )
        username = attrs.get('username', )

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric charcters only')
       
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email',)
        password = attrs.get('password',)

        user = authenticate(email=email, password=password)
        if not user.is_active:
            raise AuthenticationFailed('Accont is not activated')
        if not user.is_verified:
            raise AuthenticationFailed('email is not verified')
        if not user:
            raise AuthenticationFailed('Invalid creadential, try agin ')

        return{
            'email': user.email,
            'username': user.username,
            'tokens':
        }
        return super().validate(attrs)