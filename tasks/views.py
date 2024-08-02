# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics, filters
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Task
# from .serializers import TaskSerializer
# from .filters import TaskFilter
# from final_project_backend.permissions import IsOwnerOrReadOnly
# from rest_framework import status
# from datetime import date  # for our overdue count 

# class TaskList(generics.ListCreateAPIView):
#     """
#     This will list all tasks the user has and create new tasks.
#     """
#     queryset = Task.objects.all()  # Define your queryset here
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = TaskSerializer
#     filter_backends = [
#         filters.OrderingFilter,
#         filters.SearchFilter,
#         DjangoFilterBackend,
#     ]
#     filterset_class = TaskFilter

#     search_fields = [
    
#         'description',
#         'title',
#     ]

#     ordering_fields = [
#         'priority',
#         'category',
#         'start_date',  
#         'end_date',        
      
#     ]

#     def get_queryset(self):
#         queryset = Task.objects.filter(owner=self.request.user)  # Filter tasks by owner
#         completed_count = queryset.filter(completed=True).count()
#         incomplete_count = queryset.filter(completed=False).count()
#         overdue_count = queryset.filter(completed=False, start_date__lt=date.today()).count()


#         context = {
#             'completed_count': completed_count,
#             'incomplete_count': incomplete_count,
#             'overdue_count': overdue_count

            
#         }
#         return queryset  # Return filtered queryset for the current user

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             # Set the owner of the task to the current authenticated user
#             serializer.save(owner=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()  
#     permission_classes = [IsOwnerOrReadOnly]
#     serializer_class = TaskSerializer

#     def get_queryset(self):
#         return self.queryset.filter(owner=self.request.user)

#below is new 


from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from final_project_backend.permissions import IsOwnerOrReadOnly
from rest_framework import status
from datetime import date

class TaskList(generics.ListCreateAPIView):
    """
    This will list all tasks the user has and create new tasks.
    """
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = TaskFilter

    search_fields = [
        'description',
        'title',
    ]

    ordering_fields = [
        'priority',
        'category',
        'start_date',  
        'end_date',        
    ]

    def get_queryset(self):
        """
        Return the tasks for the current user.
        """
        return Task.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to return tasks along with counts.
        """
        queryset = self.get_queryset()
        completed_count = queryset.filter(completed=True).count()
        incomplete_count = queryset.filter(completed=False).count()
        overdue_count = queryset.filter(completed=False, start_date__lt=date.today()).count()

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'tasks': serializer.data,
            'completed_count': completed_count,
            'incomplete_count': incomplete_count,
            'overdue_count': overdue_count
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new task.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task.
    """
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Return the task for the current user.
        """
        return self.queryset.filter(owner=self.request.user)

