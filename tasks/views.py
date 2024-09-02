from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter


class TaskView(generics.GenericAPIView):
    """
    Handle listing, retrieving, creating, updating, and deleting tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
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
        Filter tasks to show all tasks for superusers or only tasks owned
        by the current user.
        """
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)

    def get(self, request, pk=None, *args, **kwargs):
        """
        Handle GET requests:
        - If `pk` is provided: Retrieve a specific task.
        - If `pk` is not provided: List tasks with counts of completed,
          incomplete, and overdue tasks.
        """
        if pk is not None:
            task = self.get_queryset().filter(pk=pk).first()
            if not task:
                return Response({'detail': 'Not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            self.check_object_permissions(request, task)
            serializer = self.get_serializer(task)
            return Response(serializer.data)

        queryset = self.get_queryset()
        completed_count = queryset.filter(completed=True).count()
        incomplete_count = queryset.filter(completed=False).count()
        overdue_count = queryset.filter(
            completed=False, start_date__lt=date.today()
        ).count()

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

    def put(self, request, pk=None, *args, **kwargs):
        """
        Handle PUT requests to update an existing task.
        """
        task = self.get_queryset().filter(pk=pk).first()
        if not task:
            return Response({'detail': 'Not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)
        serializer = self.get_serializer(task, data=request.data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        """
        Handle DELETE requests to remove a specific task.
        """
        task = self.get_queryset().filter(pk=pk).first()
        if not task:
            return Response({'detail': 'Not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
