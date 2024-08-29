from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task in the system.

    Attributes:
        owner (ForeignKey): The user who owns the task.
        title (CharField): The title of the task.
        description (TextField): A detailed description of the task.
        start_date (DateField): The date when the task starts.
        completed (BooleanField): Indicates if the task has been completed.
        priority (CharField): The priority level of the task. Choices are:
                              'L' for Low, 'M' for Medium, 'H' for High.
        category (CharField): The category of the task. Choices are:
                              'W' for Work, 'P' for Personal, 'O' for Other.
    """

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

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()  # Date when the task starts
    completed = models.BooleanField(default=False)  # Task completion status
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
        """
        Return a string representation of the task.

        Returns:
            str: The title of the task.
        """
        return self.title
#pepchecked