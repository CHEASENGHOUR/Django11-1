from rest_framework import serializers
from .models import Task, Submission

class TaskSerializer(serializers.ModelSerializer):
    task_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'unique_link', 'created_at', 'task_file']
        read_only_fields = ['unique_link', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    submission_file = serializers.FileField()
    student_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Submission
        fields = ['id', 'student_name', 'content', 'submission_file', 'submitted_at', 'ip_address']
        read_only_fields = ['submitted_at', 'ip_address']