from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')