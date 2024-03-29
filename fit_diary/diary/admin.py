from django.contrib import admin

from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry


# Register your models here.

@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'created_at', 'user')
    list_display_links = ('name', 'meal_type', 'created_at',)
    list_filter = ('name', 'meal_type', 'created_at', 'user')
    search_fields = ('name',)

    list_per_page = 10
    ordering = ('-created_at',)

    fieldsets = (
        ('Meal', {
            'fields': ('name', 'meal_type')
        }),
        ('Quantity', {
            'fields': ('quantity', 'unit')
        }),
        ('User', {
            'classes': ('collapse',),
            'fields': ('user',),
        }),
    )


@admin.register(DrinkEntry)
class DrinkEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'user')
    list_display_links = ('name', 'created_at',)
    list_filter = ('name', 'created_at', 'user')
    search_fields = ('name',)

    list_per_page = 10
    ordering = ('-created_at',)

    fieldsets = (
        ('Drink', {
            'fields': ('name', )
        }),
        ('Quantity', {
            'fields': ('quantity', 'unit')
        }),
        ('User', {
            'classes': ('collapse',),
            'fields': ('user',),
        }),
    )


@admin.register(WaterIntakeEntry)
class WaterIntakeEntryAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'created_at', 'user')
    list_display_links = ('quantity', 'created_at',)
    list_filter = ('created_at', 'user')

    list_per_page = 10
    ordering = ('-created_at',)

    fields = ('quantity', 'unit', 'user')
