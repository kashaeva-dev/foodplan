# Generated by Django 4.2.11 on 2024-04-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0012_subscription_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='По умолчанию'),
        ),
    ]