from rest_framework import serializers
from .models import Profile
from tasks.models import Task  # Import Task model from the 'tasks' app


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    completed_tasks_count = serializers.SerializerMethodField()
    total_tasks_count = serializers.SerializerMethodField()
    # is_owner = serializers.SerializerMethodField()  # Uncomment if needed

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'bio', 'image',
            'completed_tasks_count', 'total_tasks_count',
        ]

    def get_completed_tasks_count(self, obj):
        """
        Get the count of completed tasks for the profile's owner.
        """
        return obj.owner.tasks.filter(completed=True).count()

    def get_total_tasks_count(self, obj):
        """
        Get the total count of tasks for the profile's owner.
        """
        return obj.owner.tasks.count()
