# Generated by Django 4.1.1 on 2022-09-29 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treats', '0014_coupon_coupon_treats_coup_created_45212d_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='status',
            field=models.CharField(choices=[('Not sent yet', 'Not Sent Yet'), ('Waiting for response', 'Waiting For Response'), ('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Expired', 'Expired')], default='Not sent yet', max_length=20),
        ),
    ]
