from django import forms
from .models import User, Task
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Both fields are required.")
        return cleaned_data
    

class TeacherTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter task title (e.g., Homework Assignment 1)',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 5,
                'placeholder': 'Provide detailed instructions for the task',
                'required': True
            }),
            'task_file': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full',
                'accept': '.pdf,.doc,.docx,.txt',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_task_file(self):
        task_file = self.cleaned_data.get('task_file')
        if task_file:
            max_size = 5 * 1024 * 1024  # 5MB
            if task_file.size > max_size:
                raise forms.ValidationError("File size must be under 5MB.")
        return task_file

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance

class StudentSubmissionForm(forms.Form):
    student_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name',
        'required': True
    }))
    submission_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': '.pdf,.doc,.docx,.txt',
    }), required=True)