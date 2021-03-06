# Generated by Django 3.0.3 on 2020-02-29 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apptasks', '0031_auto_20200219_1610'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='checkpoint',
        #     name='id',
        #     field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
        #     preserve_default=False,
        # ),
        # migrations.AlterField(
        #     model_name='checkpoint',
        #     name='task',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apptasks.Task'),
        # ),
        migrations.AlterField(
            model_name='task',
            name='build_storage',
            field=models.CharField(blank=True, choices=[('1', 'None'), ('2', 'Github'), ('3', 'Heroku'), ('4', 'Github_Heroku')], default='1', max_length=50, null=True),
        ),
    ]
