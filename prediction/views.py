from django.shortcuts import render

from .utils import (
    get_descriptors,
    make_prediction
)

# Create your views here.


def start(request):
    return render(request, 'prediction/main.html')


def prediction(request):
    user_input: dict[str, str | int | float] = {
        'sequence': request.POST.get('sequence'),
        'ph': request.POST.get('ph'),
        'temp': request.POST.get('temp'),
        'cofactor': request.POST.get('cofactor'),
        'na_cl': request.POST.get('na_cl'),
        'k_cl': request.POST.get('k_cl'),
    }
    descriptors = get_descriptors(user_input=user_input)
    result = make_prediction(descriptors)
    return render(request, 'some_template.html', {'result': result})
