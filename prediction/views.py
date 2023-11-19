from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from prediction.forms import Prediction
from .utils import (
    get_descriptors,
    make_prediction
)

# Create your views here.


def result(request):
    return render(request, 'prediction/templates/prediction/result.html')


@csrf_exempt
def prediction(request):
    if request.method == 'POST':
        form = Prediction(request.POST)
        if form.is_valid():
            user_input = {
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
            # result_1 = form.cleaned_data.get('k_cl')*2/form.cleaned_data.get('na_cl')*0.01
            # result = result_1 - result_1*0.01

            return render(request, 'prediction/main.html', {'result': result, 'form': form})
    else:
        form = Prediction()
        return render(request, 'prediction/main.html', {'form': form})
