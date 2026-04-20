from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.formats.base_formats import XLSX, CSV
from .models import *



@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ["name"]