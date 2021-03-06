# Generated by Django 3.0.2 on 2020-01-14 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apptasks', '0010_auto_20200114_0929'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='apptasks.Task')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apptasks.Task')),
                ('title', models.CharField(max_length=250, verbose_name='Checkpoint')),
            ],
            options={
                'verbose_name': 'Checkpoint',
                'verbose_name_plural': 'Checkpoints',
            },
        ),
        # migrations.RemoveField(
        #     model_name='task',
        #     name='chekpoints',
        # ),
        migrations.CreateModel(
            name='CheckPointItem',
            fields=[
                ('checkpoint', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='apptasks.CheckPoint')),
                ('title', models.CharField(max_length=250, verbose_name='Проверка')),
                ('rate', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Проверка',
                'verbose_name_plural': 'Проверки',
            },
        ),
    ]
