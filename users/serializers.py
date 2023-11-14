from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "display_name", "email"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    display_name = serializers.CharField(required=True, min_length=3)

    class Meta:
        model = User
        fields = ["email", "password", "display_name"]

    def validate_email(self, value):
        # Check if email already exists
        email = value.lower()
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("A user with that email already exists.")
        return email

    def create(self, validated_data):
        user = User.objects.create_user(
            display_name=validated_data["display_name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        return value.lower()


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "receiver", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at", "sender"]
