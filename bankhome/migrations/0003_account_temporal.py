# Generated by Django 5.1.6 on 2025-03-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankhome', '0002_alter_account_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='temporal',
            field=models.TextField(blank=True, max_length=1, null=True),
        ),
    ]
