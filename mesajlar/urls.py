from django.urls import path
from . import views

urlpatterns = [
    path('', views.mesaj_listesi, name='mesaj_listesi'),
    path('ekle/', views.mesaj_ekle, name='mesaj_ekle'),
    path('mesaj/<int:pk>/', views.mesaj_detay, name='mesaj_detay'),
    path('mesaj/<int:pk>/duzenle/', views.mesaj_duzenle, name='mesaj_duzenle'),
    path('mesaj/<int:pk>/sil/', views.mesaj_sil, name='mesaj_sil'),
]