# Generated by Django 4.0.2 on 2022-02-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debates', '0003_remove_debate_public_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='voted_by_user',
            field=models.BooleanField(default=False),
        ),
    ]
