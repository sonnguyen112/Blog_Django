# Generated by Django 3.2.5 on 2022-03-18 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Blog', '0005_alter_blog_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-create_date']},
        ),
    ]
