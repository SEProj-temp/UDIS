from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q

from .forms import CourseForm, GradeForm
from .models import Courses, Grades, GradeTally
from accounts.models import Student

# Create your views here.
def course_home(request):
    
    tally = GradeTally.objects.all().order_by('semester_number').last()
    courses = Courses.objects.all()
    exclude = {}
    if request.user.is_authenticated:
        if request.user.is_student:
            exclude = Courses.objects.filter(Q(sub_grades__student = request.user.stu), Q(sub_grades__is_cleared = True) | Q(sub_grades__grade = -1))

    return render(request, 'courses/courses.html', {'courses': courses, 'exclude': exclude, 'tally': tally})


def courses_searcher(request):
    return render(request, 'courses/courses-search.html')

def course_register(request, pk = None):
    
    course = Courses.objects.filter(id = pk).first()
    student = request.user.stu
    sem_no = request.GET.get('sem_no')
    grade = Grades.objects.filter(student = student, semester_number = sem_no).last()
    last_grade = Grades.objects.filter(student = student, subject = course).last()

    cnum = 0
    backlog = False
    cleared = False

    if grade is not None:
        if grade.number_of_courses == 8:
            messages.error(request, "You can only register for a maximum of 8 courses in one semester!")
            return course_home(request)
        
        cnum = grade.number_of_courses
    else:
        cnum = 0
    
    if last_grade is not None:
        backlog = last_grade.is_backlog
        cleared = last_grade.is_cleared
        
    else:
        backlog = False
        cleared = False

    Grades.objects.create(
        student = student,
        semester_number = sem_no,
        subject = course,
        is_backlog = backlog,
        is_cleared = cleared,
        number_of_courses = cnum + 1
    )

    messages.success(request, f'Course {course.course_name} registered successfully!')
    return course_home(request)

def grade_tally(request, pk = None):

    stu = Student.objects.filter(id = pk).last()

    for sem_no in Grades.objects.filter(student = stu).order_by('semester_number').values_list('semester_number').distinct():
        sem_no = sem_no[0]

        grades = Grades.objects.filter(semester_number = sem_no, student = stu)
        totalcreds = 0
        cleared_creds = 0
        sgpa = 0
        

        for grade in grades:
            totalcreds += grade.subject.course_credits
            cleared_creds += grade.grade * grade.subject.course_credits
        
        sgpa = cleared_creds / totalcreds
        cgpa = 0
        last_total_creds = 0

        try: 
            cgpa = GradeTally.objects.all().last().cgpa
            last_total_creds = GradeTally.objects.all().last().total_creds
            
        except: pass
        
        totalcreds += last_total_creds

        cgpa = (cgpa * last_total_creds + cleared_creds) / totalcreds

        try:
            GradeTally.objects.update_or_create(

                student = stu,
                semester_number = sem_no,
                sgpa = round(sgpa, 2),
                cgpa = round(cgpa, 2),
                total_creds = totalcreds
            )
        except Exception:
            pass

    return render(request, 'home/profile.html', {'student': stu, 'tally': GradeTally.objects.last()})

class GradeUpdate(UpdateView):

    model = Grades
    form_class = GradeForm
    template_name = 'grades/addgrades.html'

    def form_valid(self, form):

        grades = form.save()
        pk = grades.student.id

        if grades:
            messages.success(self.request, f'Grade for {grades.student.user.username} in {grades.subject.course_code} added successfully!')
            return redirect('search_stu_result', pk)
        
    def form_invalid(self, form):
        print(form.is_valid(), form.errors)

class CourseCreate(CreateView):

    model = Courses
    form_class = CourseForm
    template_name = 'courses/addcourse.html'

    def form_valid(self, form):

        course = form.save()

        if course:
            messages.success(self.request, f'Course {course.course_name} added successfully!')
            return redirect('allcourses')
        
class CourseUpdate(UpdateView):

    model = Courses
    form_class = CourseForm
    template_name = 'courses/addcourse.html'

    def form_valid(self, form):
        
        user = self.request.user
        pk = self.kwargs['pk']
        course = Courses.objects.filter(id = pk).first()

        if course.course_dept != user.dept_name:
            messages.error(self.request, 'Can not edit the courses of another department!')
            return course_home(self.request)
        
        course = form.save()

        if course:
            messages.success(self.request, f'Course {course.course_name} updated successfully!')
            return redirect('allcourses')
        

class CourseSearch(ListView):

    model = Courses
    template_name = 'courses/courses.html'
    context_object_name = 'courses'
    extra_context = {'exclude': {}}

    def get_queryset(self):
        
        course_name = self.request.GET.get('course_name')
        course_code = self.request.GET.get('course_code')
        
        if course_name == '':
            if course_code == '':
                courses = Courses.objects.all()
            
            else:
                courses = Courses.objects.filter(course_code = course_code)
        else:
            if course_code == '':
                courses = Courses.objects.filter(course_name__contains = course_name)
            
            else:
                courses = Courses.objects.filter(course_name__contains = course_name, course_code = course_code)
        return courses