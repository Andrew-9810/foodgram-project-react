# Generated by Django 3.2.4 on 2023-12-06 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20231124_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ing', to='recipes.ingredient', verbose_name='Название'),
        ),
    ]
