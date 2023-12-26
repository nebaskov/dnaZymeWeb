from django.shortcuts import render
from .models import CandidatesDb
from django.core import serializers


def generation(request):
    print(request)
    if request.method == "POST":
        db_filtered = sorting_query_database(request)
        return render(request, 'generation/generation.html', {'db': db_filtered})
    db_filtered = database_filter(request)
    return render(request, 'generation/generation.html', {'db': db_filtered})


def is_valid_queryparam(param):
    return param != '' and param is not None


# def search_filter(request):
#     qs = serializers.serialize("python", CandidatesDb.objects.all())
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
    full_model = CandidatesDb.objects.all()
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
        start_query = f"select * from public.candidates where dnazyme.sequence ~* '{_query}' "
        if float_type or int_type:
            start_query = start_query + '' \
                          + f"union all select * from public.dnazyme where dnazyme.activity = '{_query}'"
        # start_query = start_query + '' \
        #                   + f"union all select * from public.dnazyme"
        filtered_model = CandidatesDb.objects.raw(start_query)
        output_fin = serializers.serialize("python", filtered_model)
        if len(output_fin) == 0:
            output_fin = serializers.serialize("python", full_model)
    return output_fin


def sorting_query_database(request):
    if 'g_sort_by_sequence_up' in request.POST.keys():
        filtered_model = CandidatesDb.objects.raw("select * from public.candidates order by sequence asc")
    if 'g_sort_by_sequence_down' in request.POST.keys():
        filtered_model = CandidatesDb.objects.raw("select * from public.candidates order by sequence desc")
    if 'g_sort_by_activity_up' in request.POST.keys():
        filtered_model = CandidatesDb.objects.raw("select * from public.candidates order by activity asc")
    if 'g_sort_by_activity_down' in request.POST.keys():
        filtered_model = CandidatesDb.objects.raw("select * from public.candidates order by activity desc")
    return serializers.serialize("python", filtered_model)
