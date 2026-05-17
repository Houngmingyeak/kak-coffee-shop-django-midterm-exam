from django import forms
from .models import Coffee


class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'category', 'description', 'price', 'image', 'image_url', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Caramel Macchiato',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the coffee...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'id_image',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/coffee-photo.jpg',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'image': 'Upload Photo',
            'image_url': 'Or paste image URL',
            'is_available': 'Available on Menu',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
