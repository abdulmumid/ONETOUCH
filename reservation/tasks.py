# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Booking


# @shared_task
# def send_email_task(subject, message):
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         ['mitalipovabdulmumid@gmail.com'],
#         fail_silently=False,
#     )


# @shared_task
# def send_booking_notification(booking_id, event_type):
#     try:
#         booking = Booking.objects.get(id=booking_id)
#     except Booking.DoesNotExist:
#         return

#     user_name = booking.user.get_full_name() or booking.user.username

#     if event_type == "created":
#         subject = "Новое бронирование"
#         message = (
#             f"Пользователь {user_name} забронировал время "
#             f"{booking.date} в {booking.time.strftime('%H:%M')} "
#             f"на автомойку '{booking.car_wash.name}'."
#         )
#     elif event_type == "deleted":
#         subject = "Отмена бронирования"
#         message = (
#             f"Пользователь {user_name} отменил бронирование "
#             f"{booking.date} в {booking.time.strftime('%H:%M')} "
#             f"на автомойку '{booking.car_wash.name}'."
#         )
#     else:
#         return

#     send_email_task.delay(subject, message)
