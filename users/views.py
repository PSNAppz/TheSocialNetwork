from rest_framework import viewsets
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    FriendRequestSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .models import FriendRequest, User

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def search(self, request):
        keyword = request.query_params.get("search", "").lower()
        queryset = self.get_search_queryset(keyword)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_search_queryset(self, keyword):
        if "@" in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(display_name__icontains=keyword)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def send_request(self, request, pk=None):
        receiver = User.objects.get(pk=pk)
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=request.user, receiver=receiver, status="sent"
        )
        if created:
            serializer = self.get_serializer(friend_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def accept_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
        friend_request.status = "accepted"
        friend_request.save()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
        friend_request.status = "rejected"
        friend_request.save()
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def list_friends(self, request):
        user = request.user
        friends = User.objects.filter(
            Q(sent_requests__receiver=user, sent_requests__status="accepted")
            | Q(received_requests__sender=user, received_requests__status="accepted")
        ).distinct()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def list_pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(
            receiver=request.user, status="sent"
        )
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)
