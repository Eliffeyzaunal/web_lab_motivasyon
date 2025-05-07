from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Mesaj, Kategori, Etiket
from .forms import MesajForm, KategoriForm

def mesaj_listesi(request):
    mesajlar = Mesaj.objects.all()
    
    # Arama işlevi
    arama_sorgusu = request.GET.get('arama', '')
    if arama_sorgusu:
        mesajlar = mesajlar.filter(
            Q(baslik__icontains=arama_sorgusu) | 
            Q(icerik__icontains=arama_sorgusu)
        )
    
    # Kategori filtresi
    kategori_id = request.GET.get('kategori', '')
    if kategori_id and kategori_id.isdigit():
        try:
            mesajlar = mesajlar.filter(kategori_id=int(kategori_id))
        except:
            pass
    
    # Tüm kategorileri al (filtreleme için)
    kategoriler = Kategori.objects.all()
    
    # kisaltilmis_icerik fonksiyonunu çağırabilmeniz için emin olun
    for mesaj in mesajlar:
        if not hasattr(mesaj, 'kisaltilmis_icerik_value'):
            mesaj.kisaltilmis_icerik_value = mesaj.kisaltilmis_icerik()
            
    context = {
        'mesajlar': mesajlar,
        'arama_sorgusu': arama_sorgusu,
        'kategoriler': kategoriler
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
            
            # ManyToMany ilişkisi için save_m2m() çağrılmalı
            form.save_m2m()
            
            messages.success(request, "Motivasyon mesajınız başarıyla eklendi!")
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
    
    # Yetkilendirme kontrolü
    if request.user != mesaj.yazar:
        messages.error(request, "Bu mesajı düzenleme yetkiniz bulunmuyor!")
        return redirect('mesaj_detay', pk=pk)
    
    if request.method == 'POST':
        form = MesajForm(request.POST, instance=mesaj)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesajınız başarıyla güncellendi!")
            return redirect('mesaj_detay', pk=pk)
    else:
        form = MesajForm(instance=mesaj)
    
    return render(request, 'mesajlar/mesaj_form.html', {
        'form': form, 
        'edit_mode': True,
        'mesaj': mesaj
    })

@login_required
def mesaj_sil(request, pk):
    mesaj = get_object_or_404(Mesaj, pk=pk)
    
    # Yetkilendirme kontrolü
    if request.user != mesaj.yazar:
        messages.error(request, "Bu mesajı silme yetkiniz bulunmuyor!")
        return redirect('mesaj_detay', pk=pk)
    
    if request.method == 'POST':
        mesaj.delete()
        messages.success(request, "Mesajınız başarıyla silindi!")
        return redirect('mesaj_listesi')
    
    return render(request, 'mesajlar/mesaj_sil.html', {'mesaj': mesaj})

def kategori_listesi(request):
    kategoriler = Kategori.objects.all()
    return render(request, 'mesajlar/kategori_listesi.html', {'kategoriler': kategoriler})

@login_required
def kategori_ekle(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni kategori başarıyla eklendi!")
            return redirect('kategori_listesi')
    else:
        form = KategoriForm()
    
    return render(request, 'mesajlar/kategori_form.html', {'form': form})

@login_required
def kategori_duzenle(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategori başarıyla güncellendi!")
            return redirect('kategori_listesi')
    else:
        form = KategoriForm(instance=kategori)
    
    return render(request, 'mesajlar/kategori_form.html', {
        'form': form,
        'edit_mode': True,
        'kategori': kategori
    })

@login_required
def kategori_sil(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    
    if request.method == 'POST':
        kategori.delete()
        messages.success(request, "Kategori başarıyla silindi!")
        return redirect('kategori_listesi')
    
    return render(request, 'mesajlar/kategori_sil.html', {'kategori': kategori})

def kategori_mesajlari(request, kategori_id):
    kategori = get_object_or_404(Kategori, pk=kategori_id)
    mesajlar = Mesaj.objects.filter(kategori=kategori)
    
    context = {
        'kategori': kategori,
        'mesajlar': mesajlar
    }
    
    return render(request, 'mesajlar/kategori_mesajlari.html', context)

def etiket_mesajlari(request, etiket_id):
    etiket = get_object_or_404(Etiket, pk=etiket_id)
    mesajlar = Mesaj.objects.filter(etiketler=etiket)
    
    context = {
        'etiket': etiket,
        'mesajlar': mesajlar
    }
    
    return render(request, 'mesajlar/etiket_mesajlari.html', context)