from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Mesaj, Kategori, Etiket
from django.utils.html import mark_safe

# Admin site adını ve başlığını değiştirme
admin.site.site_header = 'Motivasyon Mesajları Yönetim Paneli'
admin.site.site_title = 'Motivasyon Admin'
admin.site.index_title = 'Yönetim Paneline Hoş Geldiniz'

class TarihAraligi(admin.SimpleListFilter):
    """Özel bir filtre sınıfı - belirli tarih aralıklarına göre filtreler"""
    title = 'Tarih Aralığı'
    parameter_name = 'tarih_araligi'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Bugün'),
            ('yesterday', 'Dün'),
            ('this_week', 'Bu Hafta'),
            ('this_month', 'Bu Ay'),
            ('last_month', 'Geçen Ay'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(tarih__date=timezone.now().date())
        if self.value() == 'yesterday':
            return queryset.filter(tarih__date=timezone.now().date() - timedelta(days=1))
        if self.value() == 'this_week':
            start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
            return queryset.filter(tarih__date__gte=start_of_week)
        if self.value() == 'this_month':
            today = timezone.now().date()
            start_of_month = today.replace(day=1)
            return queryset.filter(tarih__date__gte=start_of_month)
        if self.value() == 'last_month':
            today = timezone.now().date()
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return queryset.filter(tarih__date__gte=first_day_last_month, tarih__date__lte=last_day_last_month)

class IcerikUzunlugu(admin.SimpleListFilter):
    """İçerik uzunluğuna göre filtreler"""
    title = 'İçerik Uzunluğu'
    parameter_name = 'icerik_uzunlugu'

    def lookups(self, request, model_admin):
        return (
            ('short', 'Kısa (0-100 karakter)'),
            ('medium', 'Orta (101-300 karakter)'),
            ('long', 'Uzun (300+ karakter)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'short':
            return queryset.filter(icerik__length__lte=100)
        if self.value() == 'medium':
            return queryset.filter(icerik__length__gt=100, icerik__length__lte=300)
        if self.value() == 'long':
            return queryset.filter(icerik__length__gt=300)

@admin.register(Mesaj)
class MesajAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'yazar', 'tarih', 'icerik_kisaltilmis', 'yorum_sayisi')
    list_filter = ('tarih', 'yazar', TarihAraligi, IcerikUzunlugu)
    search_fields = ('baslik', 'icerik', 'yazar__username')
    date_hierarchy = 'tarih'
    list_per_page = 20
    list_display_links = ('baslik',)
    readonly_fields = ('tarih', 'preview_text')
    fieldsets = (
        ('Mesaj Bilgileri', {
            'fields': ('baslik', 'icerik', 'yazar', 'kategori', 'etiketler')
        }),
        ('Önizleme', {
            'fields': ('preview_text',),
            'classes': ('collapse',)
        }),
        ('Tarih Bilgileri', {
            'fields': ('tarih',),
            'classes': ('collapse',)
        }),
    )
    
    # Liste görünümünde görüntülenecek içeriği kısaltır
    def icerik_kisaltilmis(self, obj):
        return obj.icerik[:50] + '...' if len(obj.icerik) > 50 else obj.icerik
    icerik_kisaltilmis.short_description = 'İçerik'
    
    # Mesajın HTML formatında önizlemesi
    def preview_text(self, obj):
        return mark_safe(f'<div style="padding: 10px; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 4px;">{obj.icerik}</div>')
    preview_text.short_description = 'İçerik Önizleme'
    
    # Bu mesaja bağlı yorum sayısını göstermek için
    def yorum_sayisi(self, obj):
        return 0  # Şu anda yorum özelliği olmadığı için 0 döner
    yorum_sayisi.short_description = 'Yorum Sayısı'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yeni bir nesne oluşturuyorsa
            obj.yazar = request.user
        super().save_model(request, obj, form, change)

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('isim', 'aciklama')
    search_fields = ('isim', 'aciklama')

@admin.register(Etiket)
class EtiketAdmin(admin.ModelAdmin):
    list_display = ('isim',)
    search_fields = ('isim',)