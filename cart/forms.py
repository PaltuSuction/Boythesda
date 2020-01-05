from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

class CartAddProductForm(forms.Form):
    # следует ли добавлять сумму к любому существующему значению в корзине для данного продукта (False)
    # или если существующее значение должно быть обновлено с заданным значением (True)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)