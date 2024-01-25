from django.contrib import admin

# Register your models here.
# expense_tracker/admin.py
from django.contrib import admin
from .models import Expens

@admin.register(Expens)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'amount', 'created_by')
    search_fields = ('name', 'category', 'description', 'created_by__username')
    list_filter = ('category', 'date')
    date_hierarchy = 'date'

