from celery import shared_task
from django.utils import timezone
from .models import Token

@shared_task
def delete_expired_tokens():
    now = timezone.now()
    expired_tokens = Token.objects.filter(expires_at__lt=now)
    count = expired_tokens.count()
    expired_tokens.delete()
    return f"{count} expired tokens deleted."
