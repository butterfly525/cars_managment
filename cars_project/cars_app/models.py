from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    make = models.CharField(verbose_name="Марка автомобиля", max_length=30, blank=False)
    model = models.CharField(verbose_name="Модель автомобиля", max_length=30, blank=False)
    year = models.CharField(verbose_name="Год выпуска", max_length=4, blank=False)
    description = models.TextField(verbose_name="Описание автомобиля", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name="Пользователь", blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.make} {self.model} {self.year}'
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["-updated_at"]

    @property
    def comments(self):
        return self.comments.all()

class Comment(models.Model):
    content = models.TextField(verbose_name="Содержание комментария", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, verbose_name="Автомобиль", related_name='comments', blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Автор комментария", blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]


    def __str__(self):
        return f'{self.created_at.strftime("%d.%m.%Y %H:%M")} {self.author}: "{self.content}"'