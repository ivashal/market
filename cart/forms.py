from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1,10)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES,coerce=int, label='Количество')
    # quantity = forms.IntegerField(max_value=1000, label='Количество')
    owerride = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
