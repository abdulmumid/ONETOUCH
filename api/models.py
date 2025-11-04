from django.db import models
from ckeditor.fields import RichTextField


class Onboarding(models.Model):
    title = models.CharField(("Заголовок"), max_length=200)
    description = models.CharField(("Описание"), max_length=200)
    image = models.ImageField(("Изображение"), upload_to="onboarding/")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name =("Онбординг")
        verbose_name_plural =("Онбординги")