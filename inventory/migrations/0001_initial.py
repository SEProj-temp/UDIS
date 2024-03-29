# Generated by Django 4.1.7 on 2023-04-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=200)),
                ('furniture_name', models.CharField(max_length=200, unique=True)),
                ('furniture_type', models.CharField(max_length=200)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=200)),
            ],
        ),
    ]
