from django import forms
from app_django.cars.models import Car

class CarPriceForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 
            'version', 'year', 
            'km', 'engine', 
            'cilinder', 'color',  
            'fuel_type', 'transmission', 
            'upholstery', 'location'
        ]
        labels = {
            'year': 'Año',
            'brand': 'Marca',
            'cilinder': 'Cilindros (3-8)',
            'color': 'Color',
            'engine': 'Motor (cc)',
            'fuel_type': 'Tipo de combustible',
            'km': 'KM',
            'location': 'Ubicación',
            'model': 'Modelo',
            'transmission': 'Transmisión',
            'upholstery': 'Tapicería',
            'version': 'Versión',
        }
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min':100, "required": True}),
            'brand': forms.Select(attrs={'class': 'form-select', "required": True}),
            'cilinder': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'color': forms.Select(attrs={'class': 'form-select', "required": True}),
            'engine': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'fuel_type': forms.Select(attrs={'class': 'form-select', "required": True}),
            'km': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'location': forms.Select(attrs={'class': 'form-select', "required": True}),
            'model': forms.Select(attrs={'class': 'form-select', "required": True}),
            'transmission': forms.Select(attrs={'class': 'form-select', "required": True}),
            'upholstery': forms.Select(attrs={'class': 'form-select', "required": True}),
            'version': forms.Select(attrs={'class': 'form-select', "required": True}),
        }
        
        def clean_year(self):
            year = self.cleaned_data.get('year')
            if year is not None and year < 1900:
                raise forms.ValidationError("Year cannot be negative.")
            return year

        def clean_km(self):
            km = self.cleaned_data.get('km')
            if km is not None and km < 0:
                raise forms.ValidationError("KM cannot be negative.")
            return km

        def clean_engine(self):
            engine = self.cleaned_data.get('engine')
            if engine is not None and engine < 0:
                raise forms.ValidationError("Engine size cannot be negative.")
            return engine
        
        def clean_brand(self):
            brand = self.cleaned_data.get('brand')
            if not brand:
                self.add_error('brand', 'Please select a brand.')