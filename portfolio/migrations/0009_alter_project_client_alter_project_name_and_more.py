# Generated by Django 4.0 on 2025-02-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_alter_subservices_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='subservices',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='team',
            name='role',
            field=models.CharField(max_length=500),
        ),
    ]
