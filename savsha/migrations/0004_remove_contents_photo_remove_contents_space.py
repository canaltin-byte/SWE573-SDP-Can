# Generated by Django 4.1.3 on 2022-11-27 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savsha', '0003_contents_alter_category_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contents',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='contents',
            name='space',
        ),
    ]