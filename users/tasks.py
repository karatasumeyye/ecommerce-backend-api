import logging

from celery import shared_task

from .services import (
    send_email_verification_email,
    send_password_reset_email,
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, user_id):
    """Send password reset email in the background."""
    try:
        send_password_reset_email(user_id)
    except Exception as exc:
        logger.exception(
            "Failed to send password reset email for user_id=%s",
            user_id,
        )
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_verification_email_task(self, user_id):
    """Send verification email in the background."""
    try:
        send_email_verification_email(user_id)
    except Exception as exc:
        logger.exception(
            "Failed to send verification email for user_id=%s",
            user_id,
        )
        raise self.retry(exc=exc)
