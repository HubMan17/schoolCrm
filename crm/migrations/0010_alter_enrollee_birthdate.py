# Generated by Django 5.0.1 on 2024-02-04 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_alter_enrolleeprofile_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='birthDate',
            field=models.DateField(null=True),
        ),
    ]
