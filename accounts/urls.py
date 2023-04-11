from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login_user, name = 'login_user'),
	path('logout/', views.logout_user, name = 'logout_user'),
        path('student/home/', views.student_home, name = 'student_home'),
        path('faculty/home/', views.faculty_home, name = 'faculty_home'),
        path('secretary/home/', views.secretary_home, name = 'secretary_home'),
	path('student-register/', views.StudentRegister.as_view(), name = 'student_register'),
	path('faculty-register/', views.FacultyRegister.as_view(), name = 'faculty_register'),
        path('secretary-register/', views.SecretaryRegister.as_view(), name = 'secretary_register'),
        path('student/search/', views.student_searcher, name = 'stusearch'),
        path('student/active-grades/<int:pk>', views.StudentActiveSearch.as_view(), name = 'active_grades'),
        path('student/search-result/', views.StudentSearchTable.as_view(), name = 'search_stu'),
        path('student/search-result/<int:pk>', views.StudentSearch.as_view(), name = 'search_stu_result'),
]
