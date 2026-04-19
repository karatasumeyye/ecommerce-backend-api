from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .tokens import email_verification_token_generator, encode_uid
from django.core.mail import send_mail
User = get_user_model()


def get_user_by_email(email):
    """Return user if found, otherwise None."""
    return User.objects.filter(email=email).first()


def build_password_reset_payload(user):
    """Prepare password reset token payload."""
    return {
        "uid": encode_uid(user),
        "token": PasswordResetTokenGenerator().make_token(user),
    }


def build_email_verification_payload(user):
    """Prepare email verification token payload."""
    return {
        "uid": encode_uid(user),
        "token": email_verification_token_generator.make_token(user),
    }


def build_password_reset_link(user):
    """Build a reset link for debugging or future frontend integration."""
    payload = build_password_reset_payload(user)
    return (
        f"{settings.BACKEND_BASE_URL}/api/users/password-reset/confirm/"
        f"?uid={payload['uid']}&token={payload['token']}"
    )

def build_email_verification_link(user):
    """Build a verification link for debugging or future frontend integration."""
    payload = build_email_verification_payload(user)
    return (
        f"{settings.BACKEND_BASE_URL}/api/users/email-verification/confirm/"
        f"?uid={payload['uid']}&token={payload['token']}"
    )

def send_password_reset_email(user_id):
    """Generate and send the password reset email."""
    user = User.objects.get(pk=user_id)
    payload = build_password_reset_payload(user)

    subject = "Reset your password"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        "We received a request to reset your password.\n\n"
        "Use the following values in the password reset confirm endpoint.\n"
        "This endpoint expects a POST request, so the values should be sent as JSON.\n\n"
        f"UID: {payload['uid']}\n"
        f"Token: {payload['token']}\n\n"
        "If you did not request this action, you can ignore this email."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_email_verification_email(user_id):
    """Generate and send the email verification email."""
    user = User.objects.get(pk=user_id)

    if user.is_email_verified:
        return

    payload = build_email_verification_payload(user)

    subject = "Verify your email address"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        "Please verify your email address using the values below.\n"
        "This endpoint expects a POST request, so the values should be sent as JSON.\n\n"
        f"UID: {payload['uid']}\n"
        f"Token: {payload['token']}\n\n"
        "Use these values in the email verification confirm endpoint."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
