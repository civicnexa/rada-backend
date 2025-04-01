# Generated by Django 5.0.7 on 2025-02-04 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('readOnly', 'readOnly')], default='readOnly', max_length=100),
        ),
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=8)),
                ('createdOn', models.DateTimeField(auto_now_add=True, null=True)),
                ('verifiedOn', models.DateTimeField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('verification_type', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='otp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
