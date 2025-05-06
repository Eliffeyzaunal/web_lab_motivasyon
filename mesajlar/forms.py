from django import forms
from .models import Mesaj

class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['baslik', 'icerik']