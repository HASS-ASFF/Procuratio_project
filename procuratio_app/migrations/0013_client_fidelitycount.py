# Generated by Django 4.2.7 on 2023-12-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procuratio_app', '0012_rendezvous_reservation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='fidelitycount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
