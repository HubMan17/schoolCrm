# Generated by Django 5.0.1 on 2024-02-04 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_enrolleeprofile_status_alter_cardhistory_changedate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='copyPassport',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='copySNILS',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='documentOfEducation',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='medicalDoc_086_y',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='medicalDoc_29_H',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='medicalInsurance',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='passport',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='photo_3_x_4',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='enrollee',
            name='middleName',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='enrolleeprofile',
            name='code',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='enrolleeprofile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='enrolleeprofile',
            name='password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='enrolleeprofile',
            name='phone',
            field=models.CharField(default='', max_length=100),
        ),
    ]
