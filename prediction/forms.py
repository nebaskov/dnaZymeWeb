from django import forms


class Prediction(forms.Form):
    sequence = forms.CharField(max_length=96)
    ph = forms.FloatField(max_value=15, min_value=0)
    temp = forms.FloatField()
    cofactor = forms.CharField()
    na_cl = forms.FloatField()
    k_cl = forms.FloatField()
