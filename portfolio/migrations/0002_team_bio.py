# Generated by Django 5.0.7 on 2025-01-28 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='bio',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
