# Generated by Django 4.0.2 on 2022-02-10 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debate',
            name='public_id',
        ),
    ]
