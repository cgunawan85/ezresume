# Generated by Django 2.1.1 on 2018-10-05 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0005_auto_20181005_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workexperience',
            old_name='description',
            new_name='achievements',
        ),
    ]
