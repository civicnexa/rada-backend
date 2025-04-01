from threading import Thread

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone
from rest_framework import serializers

from account.models import Subscriber, UserDetail
from rada.modules.choices import ROLE_CHOICES
from rada.modules.email_template import send_token_to_email, account_opening_email
from rada.modules.exceptions import InvalidRequestException
from rada.modules.utils import (
    api_response,
    generate_random_password,
    log_request,
    get_next_minute,
    generate_random_otp,
    encrypt_text,
    password_checker,
    decrypt_text,
    sendEmail,
)


class UserSerializerOut(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    lastLogin = serializers.CharField(source="last_login")
    dateJoined = serializers.CharField(source="date_joined")
    image = serializers.CharField(source="userdetail.image.url")
    role = serializers.CharField(source="userdetail.role")
    phoneNumber = serializers.CharField(source="userdetail.phoneNumber")

    class Meta:
        model = User
        exclude = [
            "is_staff",
            "is_superuser",
            "password",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "last_login",
            "date_joined",
        ]


class UserSerializerIn(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    emailAddress = serializers.EmailField()
    phoneNumber = serializers.CharField(max_length=15, required=False)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    institutionId = serializers.CharField(required=False)
    auth_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        first_name = validated_data.get("firstName")
        last_name = validated_data.get("lastName")
        email_address = validated_data.get("emailAddress")
        phone_number = validated_data.get("phoneNumber")
        acct_type = validated_data.get("role")
        request_user = validated_data.get("auth_user")
        success = True

        logged_in_user = UserDetail.objects.get(user=request_user)

        # Check if role is "risk"
        if acct_type == "admin":
            message, success = (
                "You are not permitted to perform this action:  ADMIN CREATION",
                False,
            )

        # Check if user with email exists
        if User.objects.filter(email__iexact=email_address).exists():
            message, success = "User with this email address already exist", False

        if success is False:
            response = api_response(message=message, status=False)
            raise InvalidRequestException(response)

        # Generate random password
        random_password = generate_random_password()
        log_request(f"random password: {random_password}")

        # Create user
        user = User.objects.create(
            username=email_address,
            email=email_address,
            first_name=first_name,
            last_name=last_name,
            password=make_password(random_password),
        )

        user_profile = UserDetail.objects.create(
            user=user,
            role=acct_type,
            phoneNumber = phone_number,
            createdBy=logged_in_user.user,
        )
        
        context = {
            "username": user.username,
            "password": random_password,
            "first_name": user.first_name,
            "subject": "Admin Registration"
            
        }
        # Send OTP to user
        Thread(
            target=sendEmail, args=[context, 'welcome.html', [user.email]]
        ).start()
        print(
            UserSerializerOut(
                user, context={"request": self.context.get("request")}
            ).data
        )
        return UserSerializerOut(
            user, context={"request": self.context.get("request")}
        ).data


class LoginSerializerIn(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            response = api_response(message="Invalid email or password", status=False)
            raise InvalidRequestException(response)

        user_profile = UserDetail.objects.get_or_create(user=user)

        return user

class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"
        # exclude = ['email']