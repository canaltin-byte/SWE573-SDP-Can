# Generated by Django 4.1.3 on 2022-12-27 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savsha', '0010_delete_category_contents_origin_contents_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contents',
            name='origin',
            field=models.CharField(default='unknown', max_length=1000),
        ),
    ]