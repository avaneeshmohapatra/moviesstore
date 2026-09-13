from django.contrib import admin
from .models import Movie, Review
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
class ReviewAdmin(admin.ModelAdmin):
    reported_fields = ['user', 'movie', 'id', 'is_reported', 'date']
    reported_filter = ['is_reported=True']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
