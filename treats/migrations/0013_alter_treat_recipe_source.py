# Generated by Django 4.1.1 on 2022-09-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treats', '0012_treat_recipe_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treat',
            name='recipe_source',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
