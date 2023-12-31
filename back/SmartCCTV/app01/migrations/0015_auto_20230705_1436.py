# Generated by Django 3.2.13 on 2023-07-05 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_allcctv_update_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allcctv',
            options={'verbose_name': 'cctv', 'verbose_name_plural': 'cctv'},
        ),
        migrations.AlterModelOptions(
            name='class_info',
            options={'verbose_name': '班级信息', 'verbose_name_plural': '班级信息'},
        ),
        migrations.AlterModelOptions(
            name='student_daily_data',
            options={'verbose_name': '数据', 'verbose_name_plural': '数据'},
        ),
        migrations.AlterModelOptions(
            name='student_info',
            options={'verbose_name': '学生信息', 'verbose_name_plural': '学生信息'},
        ),
        migrations.AlterModelOptions(
            name='teacher_account',
            options={'verbose_name': '教师管理', 'verbose_name_plural': '教师管理'},
        ),
        migrations.AlterModelOptions(
            name='teacher_class',
            options={'verbose_name': '教师类', 'verbose_name_plural': '教师类'},
        ),
        migrations.AlterModelOptions(
            name='teacher_info',
            options={'verbose_name': '教师信息', 'verbose_name_plural': '教师信息'},
        ),
    ]
