# Generated by Django 3.0.2 on 2020-01-14 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apptasks', '0014_auto_20200114_1003'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='checkpoint',
        #     name='id',
        #     field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
        #     preserve_default=False,
        # ),
        # migrations.AlterField(
        #     model_name='checkpoint',
        #     name='task',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apptasks.Task'),
        # ),
        migrations.DeleteModel(
            name='CheckPointItem',
        ),
    ]
