from django.contrib import admin

from fit_diary.workouts.models import Workout


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'category', 'intensity', 'type', 'created_at', 'user')
    list_display_links = ('pk','name', 'category', 'intensity', 'type', 'created_at',)
    list_filter = ('name', 'category', 'intensity', 'type', 'created_at', 'user')
    search_fields = ('name', 'type', 'equipment_needed', 'user')

    list_per_page = 20
    ordering = ('-created_at',)

    fieldsets = (
        ('Info', {
            'fields': ('name', 'video_url')
        }),
        ('Category', {
            'fields': ('category', 'intensity', 'type')
        }),
        ('Additional Information', {
            'fields': ('equipment_needed', 'description',),
        }),
        ('Added by', {
            'classes': ('collapse',),
            'fields': ('user', ),
        }),
    )
