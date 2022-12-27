# Generated by Django 4.1.3 on 2022-12-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savsha', '0009_extendeduser_remove_contents_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='contents',
            name='origin',
            field=models.CharField(default='unknown', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='contents',
            name='private',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
