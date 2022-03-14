from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User

STATES = [
        ('init', 'init'),
        ('inprogress', 'inprogress'),
        ('finished', 'finished')
    ]
PRIORITY = [
        ('S', 'S'),
        ('A+', 'A+'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

class Task(models.Model):
    def get_priority_list(self):
        return [item[0] for item in self.PRIORITY]

    def get_state_list(self):
        return [item[0] for item in self.STATES]
    
    def priority_validator(value):
        if value not in [item[0] for item in PRIORITY]:
            raise ValueError("Invalid priority")

    def status_validator(value):
        if value not in [item[0] for item in STATES]:
            raise ValueError("Invalid status")
    
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(null=False, default='', max_length=200)
    description = models.CharField(null=True, max_length=500)
    user = models.ForeignKey(
        User, 
        verbose_name="user_id", 
        db_column="user_id", 
        on_delete=models.SET_NULL,
        null=True,
        related_name='task',
        editable=False)
    start_time = models.DateTimeField(default=timezone.now, editable=False)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, 
                              null=False, 
                              default='init',
                              validators=[status_validator])
    priority = models.CharField(max_length=2, 
                                null=False,
                                default='B',
                                validators=[priority_validator])
    progress = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=False, 
        default=0)


class TaskLog(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    task = models.ForeignKey(
        Task,
        verbose_name="task_id",
        db_column="taks_id",
        on_delete=models.CASCADE,
        related_name='logs'
    )
    time = models.DateTimeField(default=timezone.now, editable=False)
    notes = models.CharField(null=True, max_length=400)
    progress_flag = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=False, 
        default=0)
