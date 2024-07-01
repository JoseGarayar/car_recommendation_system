from django import forms
from app_django.cars.models import Car

class CarPriceForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['year', 'brand', 'cilinder', 'color', 'engine', 'fuel_type', 'km', 'location', 'model', 'transmission', 'upholstery', 'version']
        labels = {
            'year': 'Year',
            'brand': 'Brand',
            'cilinder': 'Cilinder',
            'color': 'Color',
            'engine': 'Engine',
            'fuel_type': 'Fuel Type',
            'km': 'KM',
            'location': 'Location',
            'model': 'Model',
            'transmission': 'Transmission',
            'upholstery': 'Upholstery',
            'version': 'Version',
        }
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'cilinder': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'engine': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'transmission': forms.TextInput(attrs={'class': 'form-control'}),
            'upholstery': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
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