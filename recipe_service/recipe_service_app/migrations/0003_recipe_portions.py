# Generated by Django 5.1.3 on 2024-11-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_service_app', '0002_alter_recipe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='portions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
