# Generated by Django 4.0.3 on 2022-03-01 14:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers_remove_user_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='private_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
