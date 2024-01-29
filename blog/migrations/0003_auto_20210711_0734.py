# Generated by Django 3.2.4 on 2021-07-11 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210710_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('General', 'General'), ('Announcement', 'Announcement'), ('Notice', 'Notice'), ('Update', 'Update'), ('Important', 'Important')], default='General', max_length=100, verbose_name='post_type'),
        ),
    ]
