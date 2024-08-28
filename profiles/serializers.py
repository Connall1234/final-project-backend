# from rest_framework import serializers
# from .models import Profile
# from tasks.models import Task  # Import Task model from the 'tasks' app



# class ProfileSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     completed_tasks_count = serializers.SerializerMethodField()
#     total_tasks_count = serializers.SerializerMethodField()
#     #is_owner = serializers.SerializerMethodField()

#     class Meta:
#         model = Profile
#         fields = [
#             'id', 'owner', 'created_at', 'updated_at', 'first_name', 'last_name', 'bio', 'image', 'completed_tasks_count', 'total_tasks_count',
#         ]


#     def get_completed_tasks_count(self, obj):
#         return obj.owner.tasks.filter(completed=True).count()

#     def get_total_tasks_count(self, obj):
#         return obj.owner.tasks.count()


# # Above works 


from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from .models import Profile
from tasks.models import Task  # Import Task model from the 'tasks' app

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    completed_tasks_count = serializers.SerializerMethodField()
    total_tasks_count = serializers.SerializerMethodField()
    # is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'first_name', 'last_name', 'bio', 'image', 'completed_tasks_count', 'total_tasks_count',
        ]

    def get_completed_tasks_count(self, obj):
        return obj.owner.tasks.filter(completed=True).count()

    def get_total_tasks_count(self, obj):
        return obj.owner.tasks.count()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()
        return user

