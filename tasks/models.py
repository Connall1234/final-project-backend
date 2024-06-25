from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    
    CATEGORY_CHOICES = [
        ('W', 'Work'),
        ('P', 'Personal'),
        ('O', 'Other'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M',
)
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='O',
)
    
    
    def __str__(self):
        return self.title