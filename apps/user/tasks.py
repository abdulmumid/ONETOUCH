from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from onesignal_sdk.client import Client

@shared_task
def send_email_task(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )

@shared_task
def send_push_task(player_id, message):
    if not player_id:
        return False
    client = Client(
        app_id=settings.ONESIGNAL_APP_ID,
        rest_api_key=settings.ONESIGNAL_API_KEY
    )
    data = {
        "contents": {"en": message},
        "include_player_ids": [player_id],
    }
    try:
        return client.send_notification(data)
    except Exception as e:
        print(f"[OneSignal] Ошибка при отправке: {e}")
        return False

@shared_task
def send_user_notification(user_id, message):
    from .models import CustomUser
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        return False
    if user.email:
        send_email_task.delay(user.email, "ONETOUCH уведомление", message)
    if user.player_id:
        send_push_task.delay(user.player_id, message)
