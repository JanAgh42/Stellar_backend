# Generated by Django 4.1.7 on 2023-03-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stellar_backend', '0002_alter_signindata_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiontoken',
            name='token',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sessiontoken',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
