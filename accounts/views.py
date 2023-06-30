from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView
from django.core.exceptions import PermissionDenied

from .models import User, Student
from courses.models import Grades
from .forms import StudentSignUpForm, FacultySignUpForm, SecretarySignUpForm

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def student_searcher(request):
    return render(request, 'home/student-search.html')

def student_home(request):
    return render(request, 'home/home-student.html')

def faculty_home(request):
    return render(request, 'home/home-faculty.html')

def secretary_home(request):
    return render(request, 'home/home-secretary.html')

def student_regcomplete(request):
    student = Student.objects.all().last()
    return render(request, 'student_regComplete.html', {"student": student})

def faculty_regcomplete(request):
    faculty = User.objects.all().last()
    return render(request, 'fac_regComplete.html', {"faculty": faculty})

def secretary_regcomplete(request):
    secretary = User.objects.all().last()
    return render(request, 'sec_regComplete.html', {"secretary": secretary})

def stu_user_validate(roll_number):

    if len(roll_number) != 9: return False

    if not '0' <= roll_number[:2] <= '99':
        return False
    elif not 'AA' <= roll_number[2:4] <= 'ZZ':
        return False
    elif not '00000' <= roll_number[4:] <= '99999':
        return False
    else:
        return True

class StudentRegister(CreateView):

    model = User
    form_class = StudentSignUpForm
    template_name = 'registers/student_register.html'

    def form_valid(self, form):
        
        em = form.cleaned_data.get('email')
        #if not stu_user_validate(form.cleaned_data['username']):
        #    messages.error(self.request, "Roll number is not in the correct format!")
        #    return render(self.request, 'registers/student_register.html', {'form': form})

        if User.objects.filter(email = em).exists():
            messages.error(self.request, "User with the given email ID already exists!")
            return render(self.request, 'registers/student_register.html', {'form': form})
        
        user = form.save()
        
        if user:
            messages.success(self.request, f'Student {user.first_name} {user.last_name} added successfully!')
            return redirect('secretary_home')

class StudentSearchTable(ListView):

    model = Student
    template_name = 'home/searchstu.html'
    context_object_name = 'students'

    def get_queryset(self):
        
        roll = self.request.GET.get('r_no')
        stu_name = self.request.GET.get('stu_name')

        if roll == '':
            if stu_name == '':
                user = Student.objects.all()
            
            else:
                user = Student.objects.filter(user__first_name = stu_name)
        else:
            if stu_name == '':
                user = Student.objects.filter(user__username = roll)
            
            else:
                user = Student.objects.filter(user__username = roll, user__first_name = stu_name)
        return user

class StudentSearch(DetailView):

    model = Student
    template_name = 'home/profile.html'
    context_object_name = 'student'
    extra_context = {'distinct': Grades.objects.all().distinct('subject__course_name')}

    def dispatch(self, request, *args, **kwargs):
        user_obj = request.user
        if not (user_obj.username == self.get_object().username or user_obj.is_faculty or user_obj.is_secretary):
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class StudentActiveSearch(DetailView):
    model = Student
    template_name = 'grades/grades.html'
    context_object_name = 'student'
    extra_context = {'distinct': Grades.objects.all().distinct('subject__course_name')}

    def dispatch(self, request, *args, **kwargs):
        user_obj = request.user
        if not user_obj.username == self.get_object().username:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)
    
class FacultyRegister(CreateView):

    model = User
    form_class = FacultySignUpForm
    template_name = 'registers/faculty_register.html'

    def form_valid(self, form):
        
        em = form.cleaned_data.get('email_id')

        if User.objects.filter(email = em).exists():
            messages.error(self.request, "User with the given email ID already exists!")
            return render(self.request, 'registers/faculty_register.html', {'form': form})
        
        user = form.save()

        if user:
            messages.success(self.request, f'Faculty {user.first_name} {user.last_name} added successfully!')
            return redirect('secretary_home')

class SecretaryRegister(CreateView):

    model = User
    form_class = SecretarySignUpForm
    template_name = 'registers/secretary_register.html'
    
    def form_valid(self, form):
        
        em = form.cleaned_data.get('email_id')

        if User.objects.filter(email = em).exists():
            messages.error(self.request, "User with the given email ID already exists!")
            return render(self.request, 'registers/secretary_register.html', {'form': form})
        
        user = form.save()

        if user:
            messages.success(self.request, f'Secretary {user.first_name} {user.last_name} added successfully!')
            return redirect('secretary_home')   
            
def login_user(request):

    if request.method == 'POST':

        form = AuthenticationForm(data = request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username = username, password = password)
            if user is not None:

                login(request, user)

                if user.is_student:
                    return redirect('/student/home')
                elif user.is_faculty:
                    return redirect('/faculty/home')
                elif user.is_secretary:
                    return redirect('/secretary/home')
                else:
                    return redirect('/home')
            else:
                messages.error(request, "Invalid username or password")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html', context = {'form': AuthenticationForm()})

def logout_user(request):

    logout(request)
    return redirect('/')
