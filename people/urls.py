from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name="index"),
    path('task/', views.task, name="task"),
    # path('',  views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('submit/<uuid:unique_link>/', views.StudentSubmitView.as_view(), name='student_submit'),
    path('logout/', views.Logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
