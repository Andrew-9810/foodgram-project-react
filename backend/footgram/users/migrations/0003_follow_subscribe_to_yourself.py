# Generated by Django 3.2.4 on 2023-11-24 19:05

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20231111_1741'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('author')), _negated=True), name='subscribe_to_yourself'),
        ),
    ]
