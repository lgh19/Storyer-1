from django.urls import path

from . import views

app_name = 'storyer'
urlpatterns = [
    path('', views.index, name='index'),
    path('student-login', views.login_student, name='student-login'),
    path('login_faculty', views.login_faculty, name='login_faculty'),
    path('student-signup', views.signup_student, name='student-signup'),
    path('signup_faculty', views.signup_faculty, name='signup_faculty'),
    path('student-home/<int:student_id>/',
         views.student_home, name='student-home'),
    path('groups/<int:student_id>/', views.pick_groups,
         name='student-pick-groups'),
]
