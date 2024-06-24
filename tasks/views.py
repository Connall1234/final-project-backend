from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from final_project_backend.permissions import IsOwnerOrReadOnly


class TaskList(APIView):
    """
    This will list all profiles we have
    """
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetail(APIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk): 
        try:
            tasks = Task.objects.get(pk=pk)
            return tasks
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(self.request, task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)