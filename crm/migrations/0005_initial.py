# Generated by Django 5.0.1 on 2024-01-29 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0004_remove_group_idspecialties_remove_student_idgroup_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport', models.ImageField(upload_to='images/')),
                ('copyPassport', models.ImageField(upload_to='images/')),
                ('documentOfEducation', models.ImageField(upload_to='images/')),
                ('photo_3_x_4', models.ImageField(upload_to='images/')),
                ('medicalDoc_086_y', models.ImageField(upload_to='images/')),
                ('medicalDoc_29_H', models.ImageField(upload_to='images/')),
                ('copySNILS', models.ImageField(upload_to='images/')),
                ('medicalInsurance', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EnrolleeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Specialties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('position', models.IntegerField()),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('login', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('course', models.IntegerField()),
                ('subCourse', models.IntegerField()),
                ('idSpecialties', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.specialties')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('middleName', models.CharField(max_length=200)),
                ('birthDate', models.DateField()),
                ('idDocument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.document')),
                ('typeOfEducation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.education')),
                ('idEnrolleeProfile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.enrolleeprofile')),
                ('idSpecialties', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.specialties')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('middleName', models.CharField(max_length=200)),
                ('birthDate', models.DateField()),
                ('idDocument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.document')),
                ('idEnrolleeProfile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.enrolleeprofile')),
                ('idGroup', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.group')),
                ('typeOfEducation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.education')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('idEnrollee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.enrollee')),
                ('idStage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.studentboard')),
            ],
        ),
        migrations.CreateModel(
            name='CardHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changeData', models.DateField()),
                ('changeDate', models.DateField()),
                ('idCard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.studentcard')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.user')),
            ],
        ),
    ]
