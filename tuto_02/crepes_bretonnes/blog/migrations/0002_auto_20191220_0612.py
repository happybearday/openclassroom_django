# Generated by Django 2.2.4 on 2019-12-20 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='nom',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]