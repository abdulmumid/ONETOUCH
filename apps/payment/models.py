#Django
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model
from django.utils import timezone
#Library
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta


User = get_user_model()


class CarWash(models.Model):
    name = models.CharField("Название", max_length=100)
    phone = PhoneNumberField("Телефон", region="KG")
    address = models.CharField("Адрес", max_length=255)
    open_time = models.TimeField("Время открытия")
    closing_time = models.TimeField("Время закрытия")
    rating = models.FloatField("Рейтинг", default=0.0)
    img = models.ImageField("Изображение", upload_to='carwash_images/', blank=True, null=True)
    whatsapp = PhoneNumberField("WhatsApp", blank=True, null=True)
    instagram = models.URLField("Instagram", blank=True, null=True)
    location = gis_models.PointField("Местоположение", geography=True)

    def __str__(self):
        return f"{self.name} ({self.open_time} - {self.closing_time})"

    class Meta:
        verbose_name = "Автомойка"
        verbose_name_plural = "Автомойки"
        indexes = [
            gis_models.Index(fields=['location']),
        ]


class Subscription(models.Model):
    name = models.CharField("Название", max_length=100)
    moyka = models.IntegerField("Количество моек", default=0)
    unlimited_carwash = models.BooleanField("Неограниченное количество мойок", default=False)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    currency = models.CharField("Валюта", max_length=10)
    title = models.CharField("Информация", max_length=200)
    title_two = models.CharField("Информация 2", max_length=200)
    duration_days = models.IntegerField("Срок подписки (дней)", default=28)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="Пользователь")
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE, related_name='user_subscriptions', verbose_name="Подписка")
    start_date = models.DateField("Дата начала", editable=False)
    end_date = models.DateField("Дата окончания", editable=False)
    payment_id = models.CharField("ID платежа", max_length=100, blank=True, null=True)
    used_washes = models.IntegerField("Использовано моек", default=0)

    @property
    def active(self):
        today = timezone.now().date()
        if today > self.end_date:
            self.delete()
            return False
        return self.start_date <= today <= self.end_date

    def has_washes_left(self):
        if self.subscription.unlimited_carwash:
            return True
        return self.used_washes < self.subscription.moyka

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.start_date = timezone.now().date()
            self.end_date = self.start_date + timedelta(days=self.subscription.duration_days)
        super().save(*args, **kwargs)

        if is_new:
            Notification.objects.create(
                user=self.user,
                message=f"Вы успешно оформили подписку '{self.subscription.name}' до {self.end_date.strftime('%d.%m.%Y')}."
            )


    def __str__(self):
        return f"{self.user} - {self.subscription}"

    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Пользователь")
    car_wash = models.ForeignKey(CarWash, on_delete=models.CASCADE, related_name='bookings', verbose_name="Автомойка")
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Подписка пользователя")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    wash_done = models.BooleanField(default=False, verbose_name="Мойка выполнена")
    cancelled = models.BooleanField(default=False, verbose_name="Отменено")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        unique_together = ('car_wash', 'date', 'time')

    def __str__(self):
        return f"{self.user} - {self.car_wash} ({self.date} {self.time})"

    def clean(self):
        now = timezone.now()
        today = now.date()

        # Запрет брони в прошлом
        if self.date < today:
            raise ValidationError("Нельзя забронировать мойку в прошлом")

        # Проверка активной подписки, если бронь не отменена
        if not self.cancelled:
            active_sub = UserSubscription.objects.filter(
                user=self.user,
                start_date__lte=self.date,
                end_date__gte=self.date
            ).first()

            if not active_sub:
                raise ValidationError("Нет активной подписки на эту дату")

            if not active_sub.has_washes_left():
                raise ValidationError("Мойки по подписке закончились")

            self.user_subscription = active_sub

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        previous_state = None

        if not is_new:
            previous_state = Booking.objects.get(pk=self.pk)

        # Если существующее бронирование — проверяем, что нельзя менять прошлое
        if previous_state:
            booking_datetime = timezone.datetime.combine(previous_state.date, previous_state.time)
            booking_datetime = timezone.make_aware(booking_datetime, timezone.get_current_timezone())

            # Запрет изменения даты на прошлую
            if self.date < timezone.now().date():
                raise ValidationError("Нельзя изменить бронь на прошлую дату")

            # Запрет отмены/восстановления прошедшей мойки
            if previous_state.cancelled != self.cancelled and booking_datetime < timezone.now():
                raise ValidationError("Нельзя отменить или восстановить прошедшую мойку")

        self.clean()
        super().save(*args, **kwargs)

        # Новое бронирование — списываем мойку
        if is_new and not self.cancelled and self.user_subscription:
            self.user_subscription.used_washes += 1
            self.user_subscription.save()
            Notification.objects.create(
                user=self.user,
                message=f"Вы успешно записаны на {self.date.strftime('%d.%m.%Y')} в {self.time.strftime('%H:%M')}."
            )

        # Обработка изменений существующей брони
        if previous_state and self.user_subscription:
            # Отмена брони
            if not previous_state.cancelled and self.cancelled:
                if self.user_subscription.used_washes > 0:
                    self.user_subscription.used_washes -= 1
                    self.user_subscription.save()
                Notification.objects.create(
                    user=self.user,
                    message=f"Вы отменили бронирование на {self.date.strftime('%d.%m.%Y')} в {self.time.strftime('%H:%M')}."
                )

            # Восстановление брони
            elif previous_state.cancelled and not self.cancelled:
                if self.user_subscription.has_washes_left():
                    self.user_subscription.used_washes += 1
                    self.user_subscription.save()
        

    def delete(self, *args, **kwargs):
        # Возврат мойки только для будущей или текущей отмененной брони
        if self.user_subscription and not self.wash_done and not self.cancelled:
            booking_datetime = timezone.datetime.combine(self.date, self.time)
            booking_datetime = timezone.make_aware(booking_datetime, timezone.get_current_timezone())

            if booking_datetime >= timezone.now() and self.user_subscription.used_washes > 0:
                self.user_subscription.used_washes -= 1
                self.user_subscription.save()

        super().delete(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
