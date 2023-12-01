from django.shortcuts import render
from .models import MainDnaDataBase
from django.core import serializers
from django.db.models import Q


def database_home(request):
    db_filtered = database_filter(request)
    return render(request, 'database/database_home.html', {'db': db_filtered})


def is_valid_queryparam(param):
    return param != '' and param is not None


# def search_filter(request):
#     qs = serializers.serialize("python", MainDnaDataBase.objects.all())
#     _query = request.GET.get('title_or_author')
#     if is_valid_queryparam(_query):
#         qs_f = []
#         _query = str(_query)
#         for item in qs:
#             if _query in item['fields']["sequence"]:
#                 qs_f.append(item)
#             elif _query in str(item['fields']["activity"]):
#                 qs_f.append(item)
#             elif _query in str(item['fields']["year_of_publication"]):
#                 qs_f.append(item)
#         return qs_f
#     return qs


def database_filter(request):
    full_model = MainDnaDataBase.objects.all()
    _query = request.GET.get('title_or_author')
    if _query.endswith('u'):
        _query.replace('u', '')
    if is_valid_queryparam(_query):
        float_type = True
        int_type = True
        try:
            int(_query)
        except:
            int_type = False
        try:
            float(_query)
        except:
            float_type = False
        start_query = f"select * from public.dnazyme where sequence ~* '{_query}'"
        if float_type and int_type:
            start_query = start_query + '' \
                          + f"union all select * from public.dnazyme where dnazyme.year_of_publication = '{_query}'"
        if float_type:
            start_query = start_query + '' \
                          + f"union all select * from public.dnazyme where dnazyme.activity = '{_query}'"
        filtered_model = MainDnaDataBase.objects.raw(start_query)
        output_fin = serializers.serialize("python", filtered_model)
        if len(output_fin) == 0:
            output_fin = serializers.serialize("python", full_model)
    return output_fin
