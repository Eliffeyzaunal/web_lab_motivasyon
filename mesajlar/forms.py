from django import forms
from .models import Mesaj, Kategori, Etiket

class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['baslik', 'icerik', 'kategori', 'etiketler']
        widgets = {
            'baslik': forms.TextInput(attrs={'class': 'form-control'}),
            'icerik': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'etiketler': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['isim', 'aciklama']
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }