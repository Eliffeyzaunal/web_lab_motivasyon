# Motivasyon Mesajları Uygulaması

Bu repository, Motivasyon Mesajları Uygulaması'nı içermektedir.

## Geliştirici Sorumlulukları

**Backend Geliştirme:**
- Models ve views geliştirme
- Kullanıcı girişi ve yetkilendirme
- Admin panel entegrasyonu

**Frontend Geliştirme (Proje arkadaşı):**
- Templates ve frontend geliştirme
- CSS stil ve tasarım iyileştirmeleri
- Mesaj arama ve filtreleme özellikleri

## Backend Özellikleri

- CRUD işlemleri için view fonksiyonları
- Kullanıcı yetkilendirme sistemi
- Gelişmiş admin panel entegrasyonu ve özel filtreler

## Kurulum ve Çalıştırma

1. Repository'yi klonlayın:
   ```
   git clone https://github.com/Eliffeyzaunal/web_lab_motivasyon.git
   cd web_lab_motivasyon
   ```

2. Sanal ortam oluşturun ve aktifleştirin:
   ```
   python -m venv venv
   # Windows için:
   venv\Scripts\activate
   # Linux/MacOS için:
   source venv/bin/activate
   ```

3. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. Veritabanı migrasyonlarını uygulayın:
   ```
   python manage.py migrate
   ```

5. Admin kullanıcısı oluşturun:
   ```
   python manage.py createsuperuser
   ```

6. Sunucuyu başlatın:
   ```
   python manage.py runserver
   ```

7. Tarayıcınızdan uygulamaya erişin:
   http://127.0.0.1:8000/