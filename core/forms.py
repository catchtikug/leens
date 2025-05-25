from django import forms
from .models import SideEffectReport, DrugResistanceReport

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffectReport
        exclude = ['user']
        widgets = {
            'side_effects': forms.Textarea(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'suspected_drug': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class DrugResistanceForm(forms.ModelForm):
    class Meta:
        model = DrugResistanceReport
        exclude = ['user']
        widgets = {
            'same_disease': forms.TextInput(attrs={'class': 'form-control'}),
            'first_diagnosis_method': forms.TextInput(attrs={'class': 'form-control'}),
            'second_diagnosis_method': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment_details': forms.Textarea(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
