from django.contrib import admin
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.admin import AdminSite
from django.db.models import Count
from django.template.response import TemplateResponse
from .models import Mesaj, Kategori

# Admin site adını ve başlığını değiştirme
admin.site.site_header = 'Motivasyon Mesajları Yönetim Paneli'
admin.site.site_title = 'Motivasyon Admin'
admin.site.index_title = 'Yönetim Paneline Hoş Geldiniz'

# Özel admin görünümü (istatistikler)
def admin_statistics_view(request):
    # Toplam mesaj sayısı
    total_messages = Mesaj.objects.count()
    
    # Son bir haftadaki mesajlar
    one_week_ago = timezone.now() - timedelta(days=7)
    messages_last_week = Mesaj.objects.filter(tarih__gte=one_week_ago).count()
    
    # Kullanıcı başına mesaj sayısı
    user_message_counts = Mesaj.objects.values('yazar__username').annotate(
        message_count=Count('id')
    ).order_by('-message_count')[:5]  # En çok mesaj yazan 5 kullanıcı
    
    # Aylık mesaj sayısı
    current_year = timezone.now().year
    monthly_messages = []
    for month in range(1, 13):
        month_messages = Mesaj.objects.filter(
            tarih__year=current_year,
            tarih__month=month
        ).count()
        monthly_messages.append((month, month_messages))
    
    context = {
        'title': 'Motivasyon Mesajları İstatistikleri',
        'total_messages': total_messages,
        'messages_last_week': messages_last_week,
        'user_message_counts': user_message_counts,
        'monthly_messages': monthly_messages,
    }
    
    return TemplateResponse(request, 'admin/statistics.html', context)

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
    # Mevcut özellikleri koruyun
    list_display = ('baslik', 'yazar', 'tarih', 'icerik_kisaltilmis', 'yorum_sayisi', 'created_at', 'updated_at')
    list_filter = ('tarih', 'yazar', TarihAraligi, IcerikUzunlugu)
    search_fields = ('baslik', 'icerik', 'yazar__username')
    date_hierarchy = 'tarih'
    list_per_page = 20
    list_display_links = ('baslik', 'icerik_kisaltilmis')
    readonly_fields = ('tarih', 'preview_text', 'created_at', 'updated_at')
    
    # Yeni özellikler ekleyin
    actions = ['mark_as_featured', 'export_as_csv']
    list_editable = ['yazar']  # Yazar değiştirilebilir (dikkatli kullanın)
    save_on_top = True  # Kaydet butonu sayfanın üstünde de görünür
    
    # Mesajları öne çıkan olarak işaretleme (örnek eylem)
    def mark_as_featured(self, request, queryset):
        # Normalde bu, bir 'featured' alanı gerektirir
        # queryset.update(featured=True)
        self.message_user(request, f"{queryset.count()} mesaj öne çıkan olarak işaretlendi.")
    mark_as_featured.short_description = "Seçili mesajları öne çıkan olarak işaretle"
    
    # CSV olarak dışa aktarma (örnek eylem)
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=motivasyon_mesajlari.csv'
        
        writer = csv.writer(response)
        writer.writerow(['Başlık', 'İçerik', 'Yazar', 'Tarih'])
        
        for obj in queryset:
            writer.writerow([obj.baslik, obj.icerik, obj.yazar.username, obj.tarih])
        
        self.message_user(request, f"{queryset.count()} mesaj CSV olarak dışa aktarıldı.")
        return response
    export_as_csv.short_description = "Seçili mesajları CSV olarak dışa aktar"
    
    # Liste görünümünde görüntülenecek içeriği kısaltır
    def icerik_kisaltilmis(self, obj):
        return obj.icerik[:50] + '...' if len(obj.icerik) > 50 else obj.icerik
    icerik_kisaltilmis.short_description = 'İçerik'
    
    # Bu mesaja bağlı yorum sayısını göstermek için
    # Not: Eğer yorum modeli eklerseniz bu fonksiyon işe yarar
    def yorum_sayisi(self, obj):
        return 0  # Şu anda yorum özelliği olmadığı için 0 döner
    yorum_sayisi.short_description = 'Yorum Sayısı'

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('isim', 'aciklama', 'mesaj_sayisi')
    search_fields = ('isim', 'aciklama')
    
    def mesaj_sayisi(self, obj):
        return obj.mesajlar.count()
    mesaj_sayisi.short_description = 'Mesaj Sayısı'