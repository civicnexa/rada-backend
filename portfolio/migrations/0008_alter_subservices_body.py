# Generated by Django 5.0.7 on 2025-02-11 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_testimonial_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservices',
            name='body',
            field=models.TextField(),
        ),
    ]
