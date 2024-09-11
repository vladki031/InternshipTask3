from django import forms
from .models import Product, Order

class CustomOrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['total_amount', 'products']
