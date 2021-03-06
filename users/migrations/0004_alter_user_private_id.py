# Generated by Django 4.0.2 on 2022-02-24 10:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_private_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='private_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
