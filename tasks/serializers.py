from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer handles the serialization and deserialization of Task
    instances, including fields such as `id`, `owner`, `start_date`,
    `completed`, `priority`, `category`, `title`, and `description`.

    Attributes:
        owner (ReadOnlyField): The username of the user who owns the task.
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'start_date', 'completed', 'priority', 'category',
            'title', 'description',
        ]
#pepchecked