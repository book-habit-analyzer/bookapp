from django.contrib import admin
from .models import User, Book, ReadingGoal, ReadingLog, AnalyticsSummary, CalendarHeatmapData

admin.site.register(User)
admin.site.register(Book)
admin.site.register(ReadingGoal)
admin.site.register(ReadingLog)
admin.site.register(AnalyticsSummary)
admin.site.register(CalendarHeatmapData)
