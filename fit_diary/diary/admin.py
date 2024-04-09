from django.contrib import admin

from fit_diary.diary.models import MealEntry, DrinkEntry, WaterIntakeEntry



@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'meal_type', 'created_at', 'user')
    list_display_links = ('pk','name', 'meal_type', 'created_at',)
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
    list_display = ('pk','name', 'created_at', 'user')
    list_display_links = ('pk','name', 'created_at',)
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
    list_display = ('pk','quantity', 'created_at', 'user')
    list_display_links = ('pk','quantity', 'created_at',)
    list_filter = ('created_at', 'user')

    list_per_page = 10
    ordering = ('-created_at',)

    fields = ('quantity', 'unit', 'user')
