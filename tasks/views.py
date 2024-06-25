from django.http import Http404
from rest_framework.permissions import IsAuthenticated

from rest_framework import status, permissions
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from final_project_backend.permissions import IsOwnerOrReadOnly

###
# class TaskList(APIView):
#     """
#     This will list all profiles we have
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         tasks = Task.objects.filter(owner=request.user)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)


# class TaskDetail(APIView):
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get_object(self, request): 
#         try:
#             tasks = Task.objects.filter(owner=request.user)
#             return tasks 
#         except Task.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         task = self.get_object(pk)
#         self.check_object_permissions(self.request, task)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
    

#     def put(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

####
class TaskList(generics.ListCreateAPIView):
    """
    This will list all tasks the user has and create new tasks.
    """
    queryset = Task.objects.all()  # Define your queryset here
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)  # Filter tasks by owner
        completed_count = queryset.filter(completed=True).count()
        incomplete_count = queryset.filter(completed=False).count()
        
        context = {
            'completed_count': completed_count,
            'incomplete_count': incomplete_count,
        }
        return queryset  # Return filtered queryset for the current user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Set the owner of the task to the current authenticated user
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()  # Define your queryset here
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)