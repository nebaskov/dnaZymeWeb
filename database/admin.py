from .models import MainDnaDataBase
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(MainDnaDataBase)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('name', 'catalytic_core', 'buffer', 'metal_ions', 'kobs', 'doi')
