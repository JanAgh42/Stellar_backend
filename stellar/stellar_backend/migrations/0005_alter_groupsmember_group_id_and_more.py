# Generated by Django 4.1.7 on 2023-03-26 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stellar_backend', '0004_alter_group_owner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsmember',
            name='group_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='groupsmember',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='group_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='reply_to_id',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
