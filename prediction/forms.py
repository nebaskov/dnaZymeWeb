from django import forms
from django.core.exceptions import ValidationError


class Prediction(forms.Form):
    sequence = forms.CharField(
        max_length=96,
        required=True,
        # label='DNA sequence',
        label='',
        initial='CCCTATACAAGTGGGAGGATTAGCCATAGGCGTGGGGCAA',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'sequence_form',
                'id': 'sequence',
                'name': 'sequence',
                # 'placeholder': 'DNA sequence'
            }
        )
    )
    ph = forms.FloatField(
        max_value=15,
        min_value=0,
        required=True,
        # label='pH',
        label='',
        initial=7.5,
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'ph_form',
                'id': 'ph',
                'name': 'ph',
                # 'placeholder': 'pH'
            }
        )
    )
    temp = forms.FloatField(
        required=True,
        # label='Temperature',
        label_suffix='',
        initial=37,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'temp_form',
                'id': 'cofactor_element',
                'name': 'cofactor_element',
#                 # 'placeholder': 'Temperature, °C'
            }
        )
    )
    cofactor_element = forms.CharField(
        required=True,
        # label='Cofactor',
        label='',
        initial='Mg',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'cofactor_form',
                'id': 'cofactor_element',
                'name': 'cofactor_element',
                # 'placeholder': 'Cofactor'
            }
        )
    )
    cofactor_concentraion = forms.CharField(
        required=True,
        label_suffix='',
        initial=0.04,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'cofactore_concentration_form',
                'id': 'cofactor_concentration',
                'name': 'cofactor_concentration',
                # 'placeholder': 'Cofactor concentratione'
            }
        )
    )
    na_cl = forms.FloatField(
        required=True,
        # label='NaCl',
        label='',
        initial=0.15,
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'nacl_form',
                'id': 'na_cl',
                'name': 'na_cl',
                # 'placeholder': 'NaCl'
            }
        )
    )
    k_cl = forms.FloatField(
        required=True,
        # label='KCl',
        label='',
        initial=0.00,
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'kcl_form',
                'id': 'k_cl',
                'name': 'k_cl',
                # 'placeholder': 'KCl'
            }
        )
    )

    def clean_sequence(self):
        sequence = self.cleaned_data['sequence']
        default_tokens = {'A', 'T', 'G', 'C'}
        format_sequence = sequence.upper()
        out_token: set[str] = set(format_sequence) - default_tokens

        if out_token:
            raise ValidationError('Invalid nucleotides in sequence!')

        if len(format_sequence) > 96:
            raise ValidationError(
                'Sequence is exceeding max length of 96 nucleotides!'
            )

        return format_sequence
