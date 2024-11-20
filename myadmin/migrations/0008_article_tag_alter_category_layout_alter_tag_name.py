# Generated by Django 5.0.8 on 2024-11-14 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0007_alter_category_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, to='myadmin.tag'),
        ),
        migrations.AlterField(
            model_name='category',
            name='layout',
            field=models.CharField(choices=[('list', 'List'), ('grid', 'Grid')], default='list', max_length=15),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]