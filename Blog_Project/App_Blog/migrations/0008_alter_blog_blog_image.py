# Generated by Django 3.2.5 on 2022-04-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0007_alter_blog_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_image',
            field=models.FileField(blank=True, upload_to='blog_images'),
        ),
    ]
