from django import forms
from .models import Mesaj, Kategori, Etiket

class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['baslik', 'icerik', 'kategori', 'etiketler']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['baslik'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Motivasyon mesajı başlığı girin'
        })
        self.fields['icerik'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Motivasyon mesajınızı buraya yazın',
            'rows': 6
        })
        self.fields['kategori'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['kategori'].empty_label = "-- Kategori Seçin --"
        self.fields['kategori'].required = False
        
        self.fields['etiketler'].widget.attrs.update({
            'class': 'form-select',
            'multiple': 'multiple'
        })
        self.fields['etiketler'].required = False

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['isim', 'aciklama']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isim'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kategori adı girin'
        })
        self.fields['aciklama'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kategori açıklaması girin',
            'rows': 3
        })