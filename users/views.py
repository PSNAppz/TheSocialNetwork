from rest_framework import viewsets
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    FriendRequestSerializer,
    UserMinSerializer,
    UserSearchSerializer,
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
from django.db.models import Q
from config.throttling import FriendRequestRateThrottle

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
        keyword = request.query_params.get("query", "").lower()
        queryset = self.get_search_queryset(keyword)
        page = self.paginate_queryset(queryset)
        serializer = UserSearchSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)

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

    @action(
        detail=False,
        methods=["post"],
        throttle_classes=[FriendRequestRateThrottle],
    )
    def send_request(self, request):
        pk = request.data.get("receiver")
        receiver = User.objects.filter(pk=pk).first()
        if not receiver:
            return Response(
                {"detail": "User does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Friend request sent."}, status=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=True, methods=["post"])
    def accept_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
        if friend_request.status != "sent":
            return Response(
                {
                    "detail": f"This friend request has already been {friend_request.status}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request.status = "accepted"
        friend_request.save()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject_request(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk, receiver=request.user)
        if friend_request.status != "sent":
            return Response(
                {
                    "detail": f"This friend request has already been {friend_request.status}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        serializer = UserMinSerializer(friends, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    @action(detail=False, methods=["get"])
    def list_pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(
            receiver=request.user, status="sent"
        )
        serializer = FriendRequestSerializer(pending_requests, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
