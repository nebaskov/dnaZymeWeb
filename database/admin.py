from .models import DnaDataBase
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(DnaDataBase)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('name', 'catalytic_core', 'buffer', 'metal_ions', 'kobs', 'doi')
