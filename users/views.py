from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import*
from .services import *
from .tokens import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .tokens import get_tokens_for_user
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_spectacular.utils import OpenApiResponse, extend_schema
from .tasks import (send_email_verification_email_task,send_password_reset_email_task)

User = get_user_model()

@extend_schema(
    tags=["Users"],
    request=SignupSerializer,
    responses={201: OpenApiResponse(description="User created successfully.")},
    summary="Register a new user",
)
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

         # Queue the verification email instead of returning debug data.
        send_email_verification_email_task.delay(user.id)

        return Response(
            {
                "message": "User created successfully. Verification email has been queued.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "is_email_verified": user.is_email_verified,
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Users"],
    request=LoginSerializer,
    responses={200: OpenApiResponse(description="Login successful.")},
    summary="Login user",
)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"message": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = get_tokens_for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "is_email_verified": user.is_email_verified,
                "tokens": tokens,
            },
            status=status.HTTP_200_OK,
        )
    

@extend_schema(
    tags=["Users"],
    request=PasswordResetRequestSerializer,
    responses={200: OpenApiResponse(description="Password reset request processed.")},
    summary="Request password reset",
    description="Generates a password reset token if the account exists.",
)
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_user_by_email(email)

     
        if user:
            # Queue the email so the request returns immediately.
            send_password_reset_email_task.delay(user.id)
            

        # Do not reveal whether the email exists.
        return Response(
            {
                "message": (
                    "If an account with this email exists, "
                    "a password reset email has been queued."
                ),
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Users"],
    request=PasswordResetConfirmSerializer,
    responses={
        200: OpenApiResponse(description="Password reset completed."),
        400: OpenApiResponse(description="Invalid or expired token."),
    },
    summary="Confirm password reset",
    description="Resets the user's password using uid and token.",
)
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = decode_uid(uid)
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response(
                {"error": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Users"],
    request=EmailVerificationRequestSerializer,
    responses={200: OpenApiResponse(description="Verification request processed.")},
    summary="Request email verification",
    description="Generates an email verification token if the account exists.",
)
class EmailVerificationRequestView(APIView):
    def post(self, request):
        serializer = EmailVerificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = get_user_by_email(email)

        # Keep request response safe and simple.
        if not user:
            return Response(
                {
                    "message": (
                        "If an account with this email exists, "
                        "a verification link has been sent."
                    )
                },
                status=status.HTTP_200_OK,
            )

        if user.is_email_verified:
            return Response(
                {"message": "Email is already verified."},
                status=status.HTTP_200_OK,
            )

        send_email_verification_email_task.delay(user.id)

        return Response(
            {
                "message": "Verification email has been queued.",
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Users"],
    request=EmailVerificationConfirmSerializer,
    responses={
        200: OpenApiResponse(description="Email verified successfully."),
        400: OpenApiResponse(description="Invalid or expired verification token."),
    },
    summary="Confirm email verification",
    description="Marks the user's email as verified using uid and token.",
)
class EmailVerificationConfirmView(APIView):
    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]

        try:
            user_id = decode_uid(uid)
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email_verification_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_email_verified:
            return Response(
                {"message": "Email is already verified."},
                status=status.HTTP_200_OK,
            )

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )
