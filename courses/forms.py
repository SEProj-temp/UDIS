from django import forms
from .models import Courses, Grades, GradeTally
from accounts.models import Student

class CourseForm(forms.ModelForm):
    '''
    A form to enter the details of a new course type
    '''

    course_name = forms.CharField(max_length = 100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Course Name'})) #Name of the course
    course_dept = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'})) #For the storage of different department names.
    course_code = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'placeholder': 'Code'})) #The head of the course, whom a student has to contact.
    course_credits = forms.IntegerField(min_value = 2, max_value = 5, required = True, widget=forms.TextInput(attrs={'placeholder': 'Credits'}))

    class Meta:

        model = Courses
        fields = '__all__'

    def save(self):

        course = super(CourseForm, self).save(commit = False)

        course.course_name = self.cleaned_data.get('course_name')
        course.course_dept = self.cleaned_data.get('course_dept')
        course.course_code = self.cleaned_data.get('course_code')
        course.course_credits = self.cleaned_data.get('course_credits')

        try:
            course.save()

        except Exception:

            Courses.objects.filter(id = course.id).delete()
            course.save()

        return course
    
class GradeForm(forms.ModelForm):
    '''
    A form to enter the grades of a subject
    '''

    student = forms.ModelChoiceField(required = True, queryset = Student.objects.all())

    semester_number = forms.IntegerField(min_value = 0, required = True)
    grade = forms.ChoiceField(required = True, choices = Grades.GRADE_CHOICES)
    subject = forms.ModelChoiceField(required = True, queryset = Courses.objects.all())

    class Meta:

        model = Grades
        fields = '__all__'

    def save(self):

        stu = self.cleaned_data.get('student')
        subject = self.cleaned_data.get('subject')
        sem_no = self.cleaned_data.get('semester_number')
        grades = Grades.objects.filter(student = stu, subject = subject, semester_number = sem_no).last()

        grades.grade = self.cleaned_data.get('grade')
        
        if grades.grade != '0':
            grades.is_cleared = True

        else:
            grades.is_backlog = True
            grades.is_cleared = False

        try:
            grades.save()

        except Exception:

            Grades.objects.filter(id = grades.id).delete()
            grades.save()

        return grades