from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'start_date', 'end_date', 'completed', 'priority', 'category'
        ]