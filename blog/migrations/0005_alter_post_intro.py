# Generated by Django 3.2.4 on 2021-07-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='intro',
            field=models.CharField(blank=True, max_length=500, verbose_name='intro'),
        ),
    ]
