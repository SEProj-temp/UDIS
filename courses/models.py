from django.db import models
from accounts.models import Student

# Create your models here.

class Courses(models.Model):
    """
    Class Courses, to store details of the various courses offered by the institute.
    """
    course_name = models.CharField(max_length = 100, unique = True)
    course_code = models.CharField(max_length = 10, unique = True)
    course_dept = models.CharField(max_length = 100)
    course_credits = models.PositiveIntegerField()

class Grades(models.Model):
    '''
    A class of models that creates the database of grades, classified by student roll numbers.
    '''

    student = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = 'stu_grades')
    semester_number = models.PositiveIntegerField()
    subject = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = 'sub_grades')

    GRADE_CHOICES = (
        (10, "EX"),
        (9, "A"),
        (8, "B"),
        (7, "C"),
        (6, "D"),
        (5, "P"),
        (0, "F"),
        (-1, "R")
    )
    
    grade = models.IntegerField(choices = GRADE_CHOICES, default = -1, null = True, blank = True)
    is_backlog = models.BooleanField(default = False)
    is_cleared = models.BooleanField(default = False)
    number_of_courses = models.PositiveIntegerField(default = 0)

    class Meta:

        unique_together = ('semester_number', 'student', 'subject')

class GradeTally(models.Model):
    '''
    Class of models that store the credit and GPA information fro eacch student.
    '''

    student = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = 'stu_tally')
    semester_number = models.PositiveIntegerField()
    sgpa = models.FloatField()
    cgpa = models.FloatField()
    total_creds = models.PositiveIntegerField()

    class Meta:

        unique_together = ('semester_number', 'student')
    
    