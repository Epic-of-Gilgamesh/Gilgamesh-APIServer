from rest_framework import serializers
from task.models import Task, TaskLog


class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog

class TaskSerializer(serializers.ModelSerializer):
    logs = TaskLogSerializer(many=True, required=False)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'start_time', 'end_time',
            'status', 'priority', 'progress', 'logs']

    # def create(self, validated_data):
    #     task = Task.objects.create(**validated_data)
    #     return album

    
