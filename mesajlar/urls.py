from django.urls import path
from . import views

urlpatterns = [
    path('', views.mesaj_listesi, name='mesaj_listesi'),
    path('ekle/', views.mesaj_ekle, name='mesaj_ekle'),
    path('mesaj/<int:pk>/', views.mesaj_detay, name='mesaj_detay'),
    path('mesaj/<int:pk>/duzenle/', views.mesaj_duzenle, name='mesaj_duzenle'),
    path('mesaj/<int:pk>/sil/', views.mesaj_sil, name='mesaj_sil'),
    
    # Kategori URL'leri
    path('kategoriler/', views.kategori_listesi, name='kategori_listesi'),
    path('kategoriler/ekle/', views.kategori_ekle, name='kategori_ekle'),
    path('kategoriler/<int:pk>/duzenle/', views.kategori_duzenle, name='kategori_duzenle'),
    path('kategoriler/<int:pk>/sil/', views.kategori_sil, name='kategori_sil'),
    path('kategoriler/<int:kategori_id>/mesajlar/', views.kategori_mesajlari, name='kategori_mesajlari'),
    
    # Etiket URL'leri
    path('etiket/<int:etiket_id>/mesajlar/', views.etiket_mesajlari, name='etiket_mesajlari'),
]