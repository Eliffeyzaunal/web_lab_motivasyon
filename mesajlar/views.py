from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import Length
from django.db.models import F
from .models import Mesaj
from .forms import MesajForm

def mesaj_listesi(request):
    mesajlar = Mesaj.objects.all()
    
    # Arama işlevi
    arama_sorgusu = request.GET.get('arama', '')
    if arama_sorgusu:
        mesajlar = mesajlar.filter(
            Q(baslik__icontains=arama_sorgusu) | 
            Q(icerik__icontains=arama_sorgusu)
        )
    
    # Tarih filtresi
    tarih_filtresi = request.GET.get('tarih', '')
    if tarih_filtresi == 'bugun':
        bugun = timezone.now().date()
        mesajlar = mesajlar.filter(tarih__date=bugun)
    elif tarih_filtresi == 'hafta':
        bir_hafta_once = timezone.now() - timedelta(days=7)
        mesajlar = mesajlar.filter(tarih__gte=bir_hafta_once)
    elif tarih_filtresi == 'ay':
        bir_ay_once = timezone.now() - timedelta(days=30)
        mesajlar = mesajlar.filter(tarih__gte=bir_ay_once)
    
    # Kullanıcı filtresi
    kullanici_filtresi = request.GET.get('kullanici', '')
    if kullanici_filtresi:
        mesajlar = mesajlar.filter(yazar__username=kullanici_filtresi)
    
    # İçerik uzunluğuna göre filtreleme
    icerik_uzunlugu = request.GET.get('icerik_uzunlugu', '')
    if icerik_uzunlugu == 'short':
        mesajlar = mesajlar.annotate(text_len=Length('icerik')).filter(text_len__lte=100)
    elif icerik_uzunlugu == 'medium':
        mesajlar = mesajlar.annotate(text_len=Length('icerik')).filter(text_len__gt=100, text_len__lte=300)
    elif icerik_uzunlugu == 'long':
        mesajlar = mesajlar.annotate(text_len=Length('icerik')).filter(text_len__gt=300)
    
    # Sıralama ekle
    siralama = request.GET.get('siralama', '')
    if siralama == 'en_yeni':
        mesajlar = mesajlar.order_by('-tarih')
    elif siralama == 'en_eski':
        mesajlar = mesajlar.order_by('tarih')
    elif siralama == 'baslik_az':
        mesajlar = mesajlar.order_by('baslik')
    elif siralama == 'baslik_za':
        mesajlar = mesajlar.order_by('-baslik')
    
    # Benzersiz kullanıcı adlarını çekelim (filtreleme için)
    tum_kullanicilar = Mesaj.objects.values_list('yazar__username', flat=True).distinct()
    
    context = {
        'mesajlar': mesajlar,
        'arama_sorgusu': arama_sorgusu,
        'tarih_filtresi': tarih_filtresi,
        'kullanici_filtresi': kullanici_filtresi,
        'tum_kullanicilar': tum_kullanicilar,
        'icerik_uzunlugu': icerik_uzunlugu,
        'siralama': siralama,
    }
    
    return render(request, 'mesajlar/mesaj_listesi.html', context)

@login_required
def mesaj_ekle(request):
    if request.method == 'POST':
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj = form.save(commit=False)
            mesaj.yazar = request.user
            mesaj.save()
            messages.success(request, 'Mesaj başarıyla eklendi.')
            return redirect('mesaj_listesi')
    else:
        form = MesajForm()
    return render(request, 'mesajlar/mesaj_form.html', {'form': form})

def mesaj_detay(request, pk):
    mesaj = get_object_or_404(Mesaj, pk=pk)
    return render(request, 'mesajlar/mesaj_detay.html', {'mesaj': mesaj})

@login_required
def mesaj_duzenle(request, pk):
    mesaj = get_object_or_404(Mesaj, pk=pk)
    
    # Yalnızca mesajın sahibi düzenleyebilir
    if request.user != mesaj.yazar:
        return HttpResponseForbidden("Bu mesajı düzenleme yetkiniz yok!")
        
    if request.method == 'POST':
        form = MesajForm(request.POST, instance=mesaj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesaj başarıyla güncellendi.')
            return redirect('mesaj_detay', pk=mesaj.pk)
    else:
        form = MesajForm(instance=mesaj)
    return render(request, 'mesajlar/mesaj_form.html', {'form': form, 'mesaj': mesaj})

@login_required
def mesaj_sil(request, pk):
    mesaj = get_object_or_404(Mesaj, pk=pk)
    
    # Yalnızca mesajın sahibi silebilir
    if request.user != mesaj.yazar:
        return HttpResponseForbidden("Bu mesajı silme yetkiniz yok!")
        
    if request.method == 'POST':
        mesaj.delete()
        messages.success(request, 'Mesaj başarıyla silindi.')
        return redirect('mesaj_listesi')
    return render(request, 'mesajlar/mesaj_sil.html', {'mesaj': mesaj})