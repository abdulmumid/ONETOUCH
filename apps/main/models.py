from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


class Onboarding(models.Model):
    title = models.CharField(("Заголовок"), max_length=200)
    description = models.CharField(("Описание"), max_length=200)
    image = models.ImageField(("Изображение"), upload_to="onboarding/")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name =("Онбординг")
        verbose_name_plural =("Онбординги")


class Marka(models.Model):
    marka = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.marka
    
    class Meta:
        verbose_name = "Марка машины"
        verbose_name_plural = "Марки машин"

class Model(models.Model):
    marka = models.ForeignKey(Marka, related_name='models', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.model}"
    
    class Meta:
        verbose_name = "Модель машины"
        verbose_name_plural = "Модели машин"

class Body(models.Model):
    kuzov = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.kuzov

    class Meta:
        verbose_name = "Кузов машины"
        verbose_name_plural = "Кузова машин"


class FAQ(models.Model):
    question = models.CharField(("Вопрос"), max_length=300)
    answer = RichTextField(("Ответ"))

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name =("Часто задаваемый вопрос")
        verbose_name_plural =("Часто задаваемые вопросы")

class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Пользователь"))
    subject = models.CharField(("Тема"), max_length=200)
    message = models.TextField(("Сообщение"))
    created_at = models.DateTimeField(("Дата создания"), auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user.email}"
    
    class Meta:
        verbose_name =("Сообщение в поддержку")
        verbose_name_plural =("Сообщения в поддержку")




#Данные машин
from django.db import models
from django.conf import settings

# Машины
class Marka(models.Model):
    marka = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.marka

class Model(models.Model):
    marka = models.ForeignKey(Marka, related_name='models', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    def __str__(self):
        return self.model

class Body(models.Model):
    kuzov = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.kuzov

# Профиль машины
class MycarProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mycar_profiles')
    marka = models.ForeignKey("main.Marka", on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey("main.Model", on_delete=models.SET_NULL, null=True)
    body = models.ForeignKey("main.Body", on_delete=models.SET_NULL, null=True)
    gos_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"Профиль Моя Машина для {self.user.email}"

class Avatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatars')
    image = models.ImageField(upload_to='avatars/')
    def __str__(self):
        return f"Аватар для {self.user.email}"