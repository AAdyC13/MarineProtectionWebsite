from django.contrib import admin

from .models import cleanText
from .models import system_config
# Register your models here.


@admin.register(cleanText)
class analysed_news(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'url')  # 在後台顯示的欄位

    search_fields = ('title', 'content', 'url', 'created_at')  # 可搜尋的欄位


@admin.register(system_config)
class system_config(admin.ModelAdmin):
    list_display = ('sysdb_name', 'sysdb_data')  # 在後台顯示的欄位
    search_fields = ('sysdb_name', 'sysdb_data')  # 可搜尋的欄位
