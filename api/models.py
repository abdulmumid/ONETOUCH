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