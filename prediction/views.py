from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from prediction.forms import Prediction
from .utils import (
    get_descriptors,
    make_prediction,
    get_seq_properties,
    process_buffer,
    get_clones,
    plot_levenshtein,
    plot_structure
)


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
            seq_properties = get_seq_properties(user_input.get('sequence'))

            context = {
                'result': make_prediction(descriptors),
                'buffer': process_buffer(user_input),
                'clones': get_clones(user_input.get('sequence')),
                'levenshtein': plot_levenshtein(user_input.get('sequence')),
                'structure': plot_structure(user_input.get('sequence'))
            }
            context.update(seq_properties)

            return render(request, 'prediction/result.html', context)
    else:
        form = Prediction()
        return render(request, 'prediction/main.html', {'form': form})