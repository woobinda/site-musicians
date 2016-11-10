from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 21)],
                                      coerce=int
                                      )

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(CartAddProductForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if not self.product.is_available(quantity=data):
            raise forms.ValidationError("Sorry, but only %(amount)s is available.",
                                        code='invalid', params={"amount": self.product.stock, })
        return data
