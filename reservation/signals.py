# # reservation/signals.py
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Booking
# from .tasks import send_booking_notification

# @receiver(post_save, sender=Booking)
# def booking_created(sender, instance, created, **kwargs):
#     if created:
#         send_booking_notification.delay(instance.id, "created")

# @receiver(post_delete, sender=Booking)
# def booking_deleted(sender, instance, **kwargs):
#     send_booking_notification.delay(instance.id, "deleted")
