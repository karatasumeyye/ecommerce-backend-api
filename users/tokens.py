from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def get_tokens_for_user(user):
    # if not user.is_active:
    #   raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Separate token generator for email verification flow."""
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.is_email_verified}{timestamp}"


email_verification_token_generator = EmailVerificationTokenGenerator()


def encode_uid(user):
    """Encode the user's ID in a URL-safe base64 format."""
    return urlsafe_base64_encode(force_bytes(user.pk))


def decode_uid(uidb64):
    """Decode the user's ID from a URL-safe base64 format."""
    return force_str(urlsafe_base64_decode(uidb64))