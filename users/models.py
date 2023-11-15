import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(unique=True, default=uuid.uuid1, max_length=50)
    display_name = models.CharField(
        "display name",
        max_length=30,
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        "phone number",
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": "A user with the same mobile number already exists. Please enter a new mobile number.",
        },
    )
    email = models.EmailField(
        "email address",
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": "This email address already exists. Please enter a new email address.",
        },
    )

    notification_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.display_name or self.uid


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    sender = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="sent")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValueError("Sender and receiver must be different.")
        super().save(*args, **kwargs)
