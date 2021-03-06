from django.apps import apps
from django import forms

Customerside = apps.get_model('admin_panel','Customerside')
Cardetails = apps.get_model('admin_panel', 'Cardetails')


class resetForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class':'form-control form-control-user'}),
        required=True,
        label='',
    )
    class Meta:
        model = Customerside
        fields = ['customerPass']
        widgets = {
            'customerPass': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }
        labels = {
            'customerPass':'',
        }


