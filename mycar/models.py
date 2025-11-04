from django.db import models


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