# Generated by Django 3.0.2 on 2020-02-18 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apptasks', '0026_auto_20200213_1203'),
        ('apporders', '0022_delete_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpointorderitem',
            name='check_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_checkpoint', to='apptasks.CheckPoint'),
        ),
    ]
