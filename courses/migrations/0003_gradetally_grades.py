# Generated by Django 4.1.7 on 2023-04-10 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_year_of_admission'),
        ('courses', '0002_alter_courses_course_code_alter_courses_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeTally',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.PositiveIntegerField()),
                ('sgpa', models.FloatField()),
                ('cgpa', models.FloatField()),
                ('total_creds', models.PositiveIntegerField()),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stu_tally', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.PositiveIntegerField()),
                ('grade', models.IntegerField(blank=True, choices=[(10, 'EX'), (9, 'A'), (8, 'B'), (7, 'C'), (6, 'D'), (5, 'P'), (0, 'F')], default=10, null=True)),
                ('is_backlog', models.BooleanField(default=False)),
                ('is_cleared', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stu_grades', to='accounts.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_grades', to='courses.courses')),
            ],
        ),
    ]