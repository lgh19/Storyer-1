from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.http import HttpResponse

from storyer.models import Student, Assignment, Faculty
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm


def index(request):
    return render(request, 'index.html')


def signup_student(request):
    if request.method == "POST":
        context = {}
        post_data = request.POST or None
        if post_data is not None:
            signup_form = SignupForm(post_data)
            if signup_form.is_valid():
                signup_form = signup_form.cleaned_data
                if not Student.objects.filter(email=signup_form['email']).exists():
                    name = (signup_form['first_name'].replace(" ", "").title(
                    ))+" "+signup_form['last_name'].replace(" ", "").title()
                    new_student = Student(
                        name=name, email=signup_form['email'], password=signup_form['password'])
                    new_student.save()
                    return student_home(request, new_student.id)
                else:
                    context.update({"exists": True})
        context.update({'error_message': True})
        return render(request, 'student-signup.html', context)

    return render(request, 'student-signup.html')


def signup_faculty(request):
    if request.method == "POST":
        context = {}
        post_data = request.POST or None
        if post_data is not None:
            signup_form = SignupForm(post_data)
            if signup_form.is_valid():
                signup_form = signup_form.cleaned_data
                if not Faculty.objects.filter(email=signup_form['email']).exists():
                    name = (signup_form['first_name'].replace(" ", "").title(
                    ))+" "+signup_form['last_name'].replace(" ", "").title()
                    new_faculty = Faculty(
                        name=name, email=signup_form['email'], password=signup_form['password'])
                    new_faculty.save()
                    return faculty_detail(request, new_faculty.id)
                else:
                    context.update({"exists": True})
        context.update({'error_message': True})
        return render(request, 'initial_faculty.html', context)

    return render(request, 'initial_faculty.html')


# student login only
def login_student(request):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            login_form = LoginForm(post_data)
            if login_form.is_valid():
                login_form = login_form.cleaned_data
                # look for student in user list
                student = Student.objects.filter(
                    email=login_form['email'], password=login_form['password']).first()
                if student is not None:
                    return student_home(request, student.id)
        context = {'error_message': True}
        return render(request, 'student-login.html', context)

    return render(request, 'student-login.html')

# faculty login only


def login_faculty(request):
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            login_form = LoginForm(post_data)
            if login_form.is_valid():
                login_form = login_form.cleaned_data
                # look for student in user list
                faculty = Faculty.objects.filter(
                    email=login_form['email'], password=login_form['password']).first()
                if faculty is not None:
                    return faculty_detail(request, faculty.id)
        context = {'error_message': True}
        return render(request, 'login-faculty.html', context)
    return render(request, 'login-faculty.html')


def student_home(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student-home.html', {'student': student})


def pick_groups(request, student_id):
    assignment_list = Assignment.objects.order_by('title')
    student = get_object_or_404(Student, pk=student_id)
    context = {
        'student': student,
        'group_list': assignment_list,
    }
    return render(request, 'student-pick.html', context)
