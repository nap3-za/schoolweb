# Generated by Django 3.2.4 on 2021-07-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_baseaccount_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseaccount',
            name='admin_no',
            field=models.IntegerField(default=0, unique=True, verbose_name='admin_no'),
        ),
    ]
