import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=Task.CATEGORY_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)

    class Meta:
        model = Task
        fields = {
            'category': ['exact'],
            'priority': ['exact'],
            'start_date': ['gte', 'lte'],
            'end_date': ['gte', 'lte'],
            'title': ['icontains'],
            'description': ['icontains'],
        }