# Generated by Django 3.2.13 on 2022-06-25 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20220625_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class_info',
            name='cctv',
            field=models.CharField(max_length=50, verbose_name='监控编号'),
        ),
        migrations.AlterModelTable(
            name='student_daily_data',
            table='student_daily_data',
        ),
    ]
