# Generated by Django 3.2.25 on 2024-12-11 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужчина'), ('female', 'Женщина')], default='female', max_length=6, verbose_name='Пол'),
            preserve_default=False,
        ),
    ]
