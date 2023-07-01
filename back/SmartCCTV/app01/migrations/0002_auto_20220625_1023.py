# Generated by Django 3.2.13 on 2022-06-25 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='class_info',
            fields=[
                ('cid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='班级编号')),
                ('grade', models.IntegerField(verbose_name='年级')),
                ('ccnumber', models.IntegerField(verbose_name='班级号')),
                ('cctv', models.IntegerField(max_length=50, verbose_name='监控编号')),
            ],
            options={
                'db_table': 'class_information',
            },
        ),
        migrations.RemoveField(
            model_name='teacher_info',
            name='id',
        ),
        migrations.AlterField(
            model_name='teacher_info',
            name='tid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app01.teacher_account'),
        ),
        migrations.CreateModel(
            name='student_info',
            fields=[
                ('sid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='学生编号')),
                ('sname', models.CharField(max_length=50, verbose_name='学生姓名')),
                ('spic', models.CharField(max_length=50, verbose_name='学生照片')),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.class_info')),
            ],
            options={
                'db_table': 'student_infomation',
            },
        ),
        migrations.CreateModel(
            name='teacher_class',
            fields=[
                ('cid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app01.class_info')),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.teacher_account')),
            ],
            options={
                'db_table': 'teacher_class',
            },
        ),
        migrations.CreateModel(
            name='student_daily_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='数据日期')),
                ('totle_time', models.FloatField(verbose_name='总时长')),
                ('up_time', models.FloatField(verbose_name='抬头时长')),
                ('down_time', models.FloatField(verbose_name='低头时长')),
                ('sleep_time', models.FloatField(verbose_name='趴下时长')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.student_info')),
            ],
            options={
                'db_table': 'student_daily_information',
                'unique_together': {('date', 'sid')},
            },
        ),
    ]
