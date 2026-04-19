from django import forms

from .models import Dispensing, Medicine, MedicineCategory, StockMovement


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        exclude = ['created_at', 'updated_at']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class DispensingForm(forms.ModelForm):
    class Meta:
        model = Dispensing
        exclude = ['unit_price', 'total_price', 'dispensed_at']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        exclude = ['medicine', 'created_at']


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }