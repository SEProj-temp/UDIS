# Generated by Django 4.1.7 on 2023-04-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_year_of_admission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='year_of_admission',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
