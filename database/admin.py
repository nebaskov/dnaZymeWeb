from .models import MainDnaDataBase
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(MainDnaDataBase)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('sequence', 'activity', 'doi')
