from django.contrib import admin
from .models import Survey

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_live', 'start_date', 'end_date')
    list_filter = ('is_live', 'start_date', 'end_date')
    search_fields = ('name', 'desc')

admin.site.register(Survey, SurveyAdmin)

# Register your models here.
