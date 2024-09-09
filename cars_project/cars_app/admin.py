from django.contrib import admin
from .models import Car, Comment

admin.site.register(Car)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_car_display', 'author', 'created_at', 'content')
    
    def get_car_display(self, obj):
        return f"{obj.car.make} {obj.car.model} {obj.car.year}"
    
    get_car_display.short_description = 'Автомобиль'