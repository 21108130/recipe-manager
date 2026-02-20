from django.contrib import admin
from .models import Category, Recipe, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'category', 'created_date', 'total_likes']
    list_filter = ['category', 'created_date']
    search_fields = ['title', 'description', 'ingredients']
    readonly_fields = ['total_likes']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location']
    search_fields = ['user__username', 'location']