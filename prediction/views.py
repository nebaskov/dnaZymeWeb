from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from prediction.forms import Prediction

from .utils import (
    get_descriptors,
    make_prediction
)

# Create your views here.


def start(request):
    return render(request, 'prediction/main.html')


@csrf_exempt
def prediction(request):
    if request.method == 'POST':
        form = Prediction(request.POST)
        if form.is_valid():
            user_input: dict[str, str | int | float] = {
                'sequence': form.cleaned_data.get('sequence'),
                'ph': form.cleaned_data.get('ph'),
                'temp': form.cleaned_data.get('temp'),
                'cofactor_element': form.cleaned_data.get('cofactor_element'),
                'cofactor_concentration': form.cleaned_data.get('cofactor_concentration'),
                'na_cl': form.cleaned_data.get('na_cl'),
                'k_cl': form.cleaned_data.get('k_cl'),
            }
            descriptors = get_descriptors(user_input=user_input)
            result = make_prediction(descriptors)
            return render(request, 'prediction/result.html', {'result': result})
    else:
        form = Prediction()
        return render(request, 'prediction/main.html', {'form': form})
