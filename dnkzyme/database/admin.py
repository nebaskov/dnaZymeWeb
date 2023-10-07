from .models import MainDataBase
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(MainDataBase)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('metal_ions', 'kobs', 'temperature', 'ph')
