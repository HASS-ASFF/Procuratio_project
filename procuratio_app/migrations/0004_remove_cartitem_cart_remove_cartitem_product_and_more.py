# Generated by Django 4.2.7 on 2023-12-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procuratio_app', '0003_remove_rendezvous_date_disponible_rendezvous_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='transaction',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='MP',
            field=models.CharField(choices=[('carte-bancaire', 'Carte Bancaire'), ('especes', 'Espèces')], max_length=150),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='produits_list',
            field=models.ManyToManyField(blank=True, to='procuratio_app.produit'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='services_list',
            field=models.ManyToManyField(blank=True, to='procuratio_app.service'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
