# Generated by Django 5.0.3 on 2024-04-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_alter_product_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
