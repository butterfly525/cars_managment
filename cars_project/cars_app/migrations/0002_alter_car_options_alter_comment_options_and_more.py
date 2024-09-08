# Generated by Django 5.1.1 on 2024-09-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание автомобиля'),
        ),
    ]
