from django import forms

PAYMENT_CHOICES = (
    ('MP', 'Mercado_Pago'),
    ('P', 'Paypal')
)

class CheckOutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Juan',
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'fernandez',
        'class': 'form-control'
    }))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Email@email.com',
        'class': 'form-control'
    }))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'11',
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Rivadavia 17000',
        'class': 'form-control'
    }))
    localidad = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Morón',
        'class': 'form-control'
    }))
    zip_code = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder':'1708',
        'class': 'form-control'
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
