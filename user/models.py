from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import random
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.apps import apps


User = settings.AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Пользователь должен иметь email"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser должен иметь is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser должен иметь is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True)
    phone = PhoneNumberField(_("Телефон"), blank=False, null=False, unique=True)
    first_name = models.CharField(_("Имя"), max_length=50)
    sur_name = models.CharField(_("Фамилия"), max_length=50, blank=True, null=True)
    is_active = models.BooleanField(_("Активен"), default=True)
    is_staff = models.BooleanField(_("Персонал"), default=False)
    is_verified = models.BooleanField(_("Подтверждён"), default=False)
    date_joined = models.DateTimeField(_("Дата регистрации"), default=timezone.now)
    player_id = models.CharField(max_length=200, blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if self.phone:
            try:
                num = phonenumbers.parse(str(self.phone), "KG")
                if not phonenumbers.is_valid_number(num):
                    raise ValidationError(_("Введите корректный номер телефона Кыргызстана (+996)"))
            except phonenumbers.NumberParseException:
                raise ValidationError(_("Введите корректный номер телефона Кыргызстана (+996)"))


class OTP(models.Model):
    PURPOSE_CHOICES = (
        ("registration", _("Регистрация")),
        ("reset_password", _("Сброс пароля")),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    code = models.CharField(_("Код"), max_length=6, blank=True)
    purpose = models.CharField(_("Назначение"), max_length=20, choices=PURPOSE_CHOICES, default="registration")
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True)
    is_used = models.BooleanField(_("Использован"), default=False)

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTP-коды")
        ordering = ["-created_at"]

    @property
    def expires_at(self):
        return self.created_at + timedelta(minutes=10)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def validate_code(self, code):
        return not self.is_used and not self.is_expired() and self.code == code

    @staticmethod
    def generate_code(length=6):
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    @classmethod
    def create_otp(cls, user, purpose="registration"):
        length = 5 if purpose == "registration" else 4
        code = cls.generate_code(length=length)
        return cls.objects.create(user=user, code=code, purpose=purpose)


class MycarProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mycar_profile')
    marka = models.ForeignKey('api.Marka', on_delete=models.SET_NULL, null=True, verbose_name=_("Марка"))
    model = models.ForeignKey('api.Model', on_delete=models.SET_NULL, null=True, verbose_name=_("Модель"))
    body = models.ForeignKey('api.Body', on_delete=models.SET_NULL, null=True, verbose_name=_("Кузов"))
    gos_number = models.CharField(("Гос. номер"), max_length=20, unique=True)

    class Meta:
        verbose_name = ("Профиль Моя Машина")
        verbose_name_plural = ("Профили Моя Машина")

    def __str__(self):
        return f"Профиль Моя Машина для {self.user.email}"


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    image = models.ImageField(("Аватар"), upload_to='avatars/')

    class Meta:
        verbose_name = ("Аватар")
        verbose_name_plural = ("Аватары")

    def __str__(self):
        return f"Аватар для {self.user.email}"
