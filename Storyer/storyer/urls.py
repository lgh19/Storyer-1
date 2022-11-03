from django.urls import path

from . import views

app_name = 'storyer'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login_faculty', views.login_faculty, name='login_faculty'),
    path('signup', views.signup, name='signup'),
    path('signup_faculty', views.signup_faculty, name='signup_faculty'),
    path('student_detail/<int:student_id>/',
         views.student_detail, name='student_detail'),
    path('groups/<int:student_id>/', views.pick_groups, name='pick_groups'),
]
