from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.formats.base_formats import XLSX, CSV
from .models import *


class MakeResource(resources.ModelResource):
    class Meta:
        model = Make
        fields = ("id", "name")
        import_id_fields = ("name")


@admin.register(Make)
class MakeAdmin(ImportExportModelAdmin):
    list_display = ["name"]
    resources = MakeResource
    format = [XLSX]
    
    
class ModelResource(resources.ModelResource):
    make = fields.Field(column_name='make', attribute='make', widget=ForeignKeyWidget(Make, 'name'))
    class Meta:
        model = Model
        fields = ("id","make","name")
        import_id_fields = ("name",)
        

@admin.register(Model)
class ModelAdmin(ImportExportModelAdmin):
    list_display = ["name"]
    resource_class = ModelResource
    format = [XLSX]
        
        
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 0
    
    
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
    list_display = ["vin", "year","fuel_type", "transmission"]
    list_filter = ["status", "fuel_type", "transmission"]