# Generated by Django 3.1.5 on 2021-12-15 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20211214_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='privateroom',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
