from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name="index"),
    path('tasks/create/', views.teacher_create_task, name='task'),
    path('tasks/created/<int:task_id>/', views.task_created, name='task_created'),
    path('tasks/<uuid:unique_link>/', views.student_task_submission, name='student_task_submission'),
    path('tasks/submission-success/', views.submission_success, name='submission_success'),
    # path('task/', views.task, name="task"),
    # path('',  views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('submit/<uuid:unique_link>/', views.StudentSubmitView.as_view(), name='student_submit'),
    path('logout/', views.Logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
