from django.db import models
from django.utils import timezone

# User model to store user data
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.TextField()
    is_profile_public = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


# Book model to store details of books added by the user
class Book(models.Model):
    STATUS_CHOICES = [
        ('Currently Reading', 'Currently Reading'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Currently Reading')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


# ReadingGoal model for tracking the user's reading goals
class ReadingGoal(models.Model):
    GOAL_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=10, choices=GOAL_CHOICES)
    target_pages = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s {self.goal_type} Goal"


# ReadingLog model to log reading progress (pages read, notes, reflections)
class ReadingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()
    pages_read = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    reflection = models.TextField(blank=True)

    def __str__(self):
        return f"Log for {self.book.title} by {self.user.username}"


# AnalyticsSummary to store user's overall reading analytics
class AnalyticsSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    total_books_read = models.PositiveIntegerField(default=0)
    total_pages_read = models.PositiveIntegerField(default=0)
    avg_pages_per_day = models.FloatField(default=0.0)
    most_read_genre = models.CharField(max_length=100, blank=True)
    current_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.user.username}"


# CalendarHeatmapData to store daily reading stats for the calendar heatmap
class CalendarHeatmapData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    pages_read = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Heatmap Data for {self.user.username} on {self.date}"
