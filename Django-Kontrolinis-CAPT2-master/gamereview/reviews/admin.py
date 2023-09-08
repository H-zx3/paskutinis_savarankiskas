from django.contrib import admin
from .models import Publisher, Game, GameReview

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher',)
    filter_horizontal = ('genre',)
    search_fields = ('title',)

@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'reviewer', 'content', 'date_created', 'rating',)
    search_fields = ('game__title', 'reviewer__username',)
    list_filter = ('date_created', 'rating',)
    list_editable = ('reviewer',)








