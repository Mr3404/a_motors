from django.contrib import admin
from .models import Banner

# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link', 'created_at')
    search_fields = ('title', 'link')
    list_filter = ('created_at',)
    
admin.site.register(Banner, BannerAdmin)