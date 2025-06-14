from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, TeacherTaskForm, StudentSubmissionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import TemplateView
# from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.urls import reverse
from .models import Task, Submission
from .serializers import TaskSerializer, SubmissionSerializer

@login_required
def teacher_create_task(request):

    if request.method == 'POST':
        form = TeacherTaskForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, "Task created successfully!")
            return redirect('task_created', task_id=task.id)
    else:
        form = TeacherTaskForm(user=request.user) 

    return render(request, 'task.html', {'form': form})

@login_required
def task_created(request, task_id):

    task = get_object_or_404(Task, id=task_id, created_by=request.user)
    task_url = request.build_absolute_uri(
        reverse('student_task_submission', args=[task.unique_link])
    )
    return render(request, 'task_created.html', {
        'task': task,
        'task_url': task_url
    })
    
def student_task_submission(request, unique_link):
    task = get_object_or_404(Task, unique_link=unique_link)

    if request.method == 'POST':
        form = StudentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = Submission(
                task=task,
                student_name=form.cleaned_data['student_name'],
                submission_file=form.cleaned_data['submission_file'],
                ip_address=request.META.get('REMOTE_ADDR')
            )
            submission.save()
            messages.success(request, "Submission received successfully!")
            return redirect('submission_success')
    else:
        form = StudentSubmissionForm()

    return render(request, 'student_submit.html', {
        'form': form,
        'task': task
    })

class StudentSubmitView(TemplateView):
    template_name = 'student_submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, unique_link=self.kwargs['unique_link'])
        context['task'] = task
        context['form'] = StudentSubmissionForm()
        return context

def submission_success(request):
    return render(request, 'submission_success.html')

# Create your views here.
@login_required(login_url='login')
def index(request):
    submissions = Submission.objects.filter(task__created_by=request.user).order_by('-submitted_at')
    return render(request, 'list.html', {'submissions': submissions})

@login_required(login_url='login')
def task(request):
    return render(request, 'task.html')

def Logout(request):
    logout(request)
    return redirect('login')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  # Allow anonymous access for compatibility

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(created_by=self.request.user)
        return Task.objects.none()

# class SubmissionViewSet(viewsets.ModelViewSet):
#     queryset = Submission.objects.all()
#     serializer_class = SubmissionSerializer
#     permission_classes = [AllowAny]

#     @action(detail=False, methods=['post'], url_path='submit/(?P<unique_link>[^/.]+)')
#     def submit_task(self, request, unique_link=None):
#         task = get_object_or_404(Task, unique_link=unique_link)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(
#                 task=task,
#                 ip_address=request.META.get('REMOTE_ADDR')
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             return Submission.objects.filter(task__created_by=self.request.user)
#         return Submission.objects.none()

class StudentSubmitView(TemplateView):
    template_name = 'student_submit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unique_link'] = self.kwargs['unique_link']
        return context



# @login_required(login_url='login')
# class AdminDashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html'
#     login_url = '/login/'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Redirect to index page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})

