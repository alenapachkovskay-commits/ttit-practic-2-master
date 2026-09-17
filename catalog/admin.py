from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import CustomUser, Category, DesignRequest



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'is_staff')
    search_fields = ('username', 'full_name', 'email')
    fields = ('username', 'full_name', 'email', 'is_staff', 'is_active')
    readonly_fields = ('username',)  # логин нельзя менять через админку

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    # При удалении категории — удалятся и заявки (благодаря CASCADE)
    # Ничего дополнительно не нужно — Django сам покажет предупреждение

class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'client', 'category', 'status')
        }),
        ('Изображения', {
            'fields': ('plan_image', 'design_image')
        }),
        ('Админка', {
            'fields': ('admin_comment',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DesignRequest, DesignRequestAdmin)


