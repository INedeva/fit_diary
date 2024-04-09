from django.contrib import admin

from fit_diary.common.models import Comment, Rating


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    COMMENT_PREVIEW_LENGTH = 10

    list_display = ('pk','short_text','created_at', 'workout', 'user')
    list_display_links = ('pk','created_at', 'workout')
    list_filter = ('workout', 'user')
    search_fields = ('text','workout', 'user')

    list_per_page = 10
    ordering = ('-created_at',)

    fields = ('text', 'workout', 'user')

    def short_text(self, obj):
        return f'{obj.text[:CommentAdmin.COMMENT_PREVIEW_LENGTH]}...' if obj.text else ''

    short_text.short_description = 'Text'  # Sets the column header in the admin list view

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'score', 'updated_at', 'created_at', 'workout', 'user')
    list_display_links = ('pk', 'score', 'updated_at')
    list_filter = ('score', 'updated_at', 'created_at', 'workout', 'user')

    list_per_page = 10
    ordering = ('-created_at',)

    fields = ('score', 'workout', 'user')
