# Generated by Django 2.1.1 on 2018-10-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0002_auto_20181003_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
