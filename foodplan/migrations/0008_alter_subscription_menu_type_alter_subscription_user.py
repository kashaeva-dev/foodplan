# Generated by Django 5.0.4 on 2024-04-18 08:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0007_subscription_subscriptionmealtype_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='menu_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='foodplan.menutype', verbose_name='Тип меню'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
