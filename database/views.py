from django.shortcuts import render
from .models import MainDnaDataBase
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def database_home(request):
    print(request)
    if request.method == "POST":
        db_filtered = sorting_query_database(request)
        return render(request, 'database/database_home.html', {'db': db_filtered})
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
    output_fin = serializers.serialize("python", full_model)
    _query = request.GET.get('title_or_author')
    if is_valid_queryparam(_query):
        if '(' in _query or ')' in _query:
            return output_fin
        _query = _query.strip()
        if _query.endswith('u'):
            _query.replace('u', '')

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

        try:
            start_query = f"select * from public.dnazyme where dnazyme.sequence ~* '{_query}' " \
                          f"union all select * from public.dnazyme where dnazyme.name ~* '{_query}'"
            if float_type and int_type:
                start_query = start_query + '' \
                              + f"union all select * from public.dnazyme where dnazyme.year_of_publication = '{_query}'"
            if float_type:
                start_query = start_query + '' \
                              + f"union all select * from public.dnazyme where dnazyme.activity = '{_query}'"
            # start_query = start_query + '' \
            #                   + f"union all select * from public.dnazyme"
            filtered_model = MainDnaDataBase.objects.raw(start_query)
            output_fin = serializers.serialize("python", filtered_model)
            if len(output_fin) == 0:
                output_fin = serializers.serialize("python", full_model)
        except:
            output_fin = serializers.serialize("python", full_model)
    return output_fin


def sorting_query_database(request):
    print(request.POST)
    if 'sort_by_name_up' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by name asc")
    if 'sort_by_name_down' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by name desc")
    if 'sort_by_sequence_up' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by sequence asc")
    if 'sort_by_sequence_down' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by sequence desc")
    if 'sort_by_activity_up' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by activity asc")
    if 'sort_by_activity_down' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by activity desc")
    if 'sort_by_temperature_up' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by temperature asc")
    if 'sort_by_temperature_down' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw("select * from public.dnazyme order by temperature desc")
    if 'sort_by_metal_ions_up' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw(
            "select * from public.dnazyme order by metal_ions asc")
    if 'sort_by_metal_ions_down' in request.POST.keys():
        filtered_model = MainDnaDataBase.objects.raw(
            "select * from public.dnazyme order by metal_ions desc")
    return serializers.serialize("python", filtered_model)
