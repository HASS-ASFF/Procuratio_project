# Generated by Django 4.2.7 on 2023-12-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procuratio_app', '0014_alter_client_code_fidelite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='fidelitycount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
