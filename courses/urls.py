from django.urls import path
from . import views

urlpatterns = [
    
    path('courses/', views.course_home, name = 'allcourses'),
    path('courses/addcourse/', views.CourseCreate.as_view(), name = 'addcourse'),
    path('courses/update/<int:pk>/', views.CourseUpdate.as_view(), name = 'course_update'),
    path('courses/search/', views.courses_searcher, name = 'course_search'),
    path('courses/search-results/', views.CourseSearch.as_view(), name = 'search_courses_result'),
    path('courses/register/<int:pk>/', views.course_register, name = 'course_register'),
    path('grades/update/<int:pk>/', views.GradeUpdate.as_view(), name = 'grade_update'),
    path('grades/tally/<int:pk>/', views.grade_tally, name = 'grade_tally'),
]