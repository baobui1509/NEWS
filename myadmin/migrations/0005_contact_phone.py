# Generated by Django 5.0.8 on 2024-11-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_contact_alter_category_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
