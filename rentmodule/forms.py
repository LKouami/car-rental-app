from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand','color','year','door','energy','air_conditionner','picture','state']
        # widgets = {
        #     'brand': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Brand"} ),
        #     'color': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Coulor"}), 
        #     'year': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Année"}), 
        #     'door': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Porte"}), 
        #     'energy': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Energie"}), 
        #     'air_conditionner': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "Air Conditionnel"}),
        #     'picture': forms.ImageField(
        #         attrs={'class': 'form-control'}),
        #     'state': forms.TextInput(
        #         attrs={'class': 'form-control',"placeholder": "State"}), 
           
        # }
       
