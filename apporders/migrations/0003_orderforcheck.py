# Generated by Django 3.0.2 on 2020-01-13 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apporders', '0002_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderForCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'Новый'), ('inprogress', 'В работе'), ('done', 'Done')], default='new', max_length=50)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apporders.Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Задача для проверки',
                'verbose_name_plural': 'Задачи для проверки',
                'ordering': ('-created',),
            },
        ),
    ]
