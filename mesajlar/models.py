from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Kategori(models.Model):
    isim = models.CharField(max_length=100, unique=True, verbose_name='Kategori Adı')
    aciklama = models.TextField(blank=True, verbose_name='Açıklama')
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['isim']
    
    def __str__(self):
        return self.isim
        
    def get_absolute_url(self):
        return reverse('kategori_mesajlari', args=[str(self.id)])

class Etiket(models.Model):
    isim = models.CharField(max_length=50, unique=True, verbose_name='Etiket Adı')
    
    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
        ordering = ['isim']
    
    def __str__(self):
        return self.isim

class Mesaj(models.Model):
    baslik = models.CharField(max_length=200, verbose_name='Başlık')
    icerik = models.TextField(verbose_name='İçerik')
    tarih = models.DateTimeField(default=timezone.now, verbose_name='Tarih')
    yazar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mesajlar', verbose_name='Yazar')
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='mesajlar', verbose_name='Kategori')
    etiketler = models.ManyToManyField(Etiket, blank=True, related_name='mesajlar', verbose_name='Etiketler')
    
    class Meta:
        verbose_name = "Motivasyon Mesajı"
        verbose_name_plural = "Motivasyon Mesajları"
        ordering = ['-tarih']
        indexes = [
            models.Index(fields=['tarih']),
            models.Index(fields=['yazar']),
        ]
    
    def __str__(self):
        return self.baslik
    
    def get_absolute_url(self):
        return reverse('mesaj_detay', args=[str(self.id)])
    
    def kisaltilmis_icerik(self):
        """İçeriğin kısaltılmış versiyonunu döndürür"""
        max_length = 100
        if len(self.icerik) > max_length:
            return self.icerik[:max_length] + '...'
        return self.icerik