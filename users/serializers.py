from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest
from django.db.models import Q

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "display_name", "email"]


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["display_name", "date_joined"]


class UserSearchSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["display_name", "email", "is_friend"]

    def get_is_friend(self, obj):
        user = self.context["request"].user
        # Check if user friend request exists and is accepted
        friend_request = FriendRequest.objects.filter(
            Q(sender=user, receiver=obj) | Q(sender=obj, receiver=user),
            status="accepted",
        ).first()
        return friend_request is not None


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

    def validate(self, data):
        if data["receiver"] == self.context["request"].user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )
        # Check if the user is already friends with the receiver
        friend_request = FriendRequest.objects.filter(
            Q(sender=self.context["request"].user, receiver=data["receiver"])
            | Q(sender=data["receiver"], receiver=self.context["request"].user),
            status="accepted",
        ).first()
        if friend_request:
            raise serializers.ValidationError("You are already friends with this user.")
        # Check if friend request already exists and is not accepted
        friend_request = FriendRequest.objects.filter(
            sender=self.context["request"].user,
            receiver=data["receiver"],
            status="sent",
        ).first()
        if friend_request:
            raise serializers.ValidationError(
                "Friend request already sent to this user."
            )
        return data
