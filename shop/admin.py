from django.contrib import admin
from .models import Coffee


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']
    ordering = ['name']
